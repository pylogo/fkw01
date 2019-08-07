from django.shortcuts import render, redirect, reverse, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
import re
from .models import User, User_Details, Withdrawals_details
from .user_serializer.serializer import UserSerializer
from django.db.models.signals import post_save
from django.dispatch import receiver
from fkw_v1.settings import REALM_NAME
from celery_task.user_task import send_register_active_email
from apps.user.interface.shop_link_password import encrypt_pk, deciphering_pk
from apps.user.interface.encypt_md5 import encrypt_md5
from django.core.cache import cache
from datetime import timedelta
from apps.user.models import Login_log
from apps.user.interface.User_Auth import User_Authentication
import logging

# log = logging.getLogger('user')  # 日志


# 用户注册
class Register(APIView):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        msg = {'code': 200, 'msg': ''}
        # 拿到前端传来的数据
        user_info = request.data
        username = user_info.get('username')
        password = user_info.get('password')
        email = user_info.get('email')
        allow = user_info.get('allow')

        # 记录日志
        ip = request.META.get('REMOTE_ADDR')
        # log.error('用户ip:%s 注册账户:%s' % (str(ip), username))

        # 判断是否同意协议
        if allow == 'false':
            msg['code'] = 20001
            msg['msg'] = '请先同意协议'
            return Response(msg)

        # 判断数据完整性
        if not all([username, password, email]):
            msg['code'] = 20002
            msg['msg'] = '数据不完整'
            return Response(msg)

        # 判断邮箱
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9]+(\.[a-z]{2,5}){1,2}$', email):
            msg['code'] = 20003
            msg['msg'] = '邮箱格式不正确'
            return Response(msg)

        # 判断账号密合法性
        if not (
                (len(username) >= 3 and len(username) < 20)
                and
                (len(password) >= 3 and len(password) < 20)
                and
                (username.isalnum() and password.isalnum())
        ):
            msg['code'] = 20004
            msg['msg'] = '用户名或密码不能小于三位且必须是数字字母组成'
            return Response(msg)

        # 判断邮箱是否重复
        if username == password:
            msg['code'] = 20005
            msg['msg'] = '用户名与密码不能相同'
            return Response(msg)

        # 判断用户名是否重复
        user = User.objects.filter(username=username)
        if user:
            msg['code'] = 20006
            msg['msg'] = '用户名已存在'
            return Response(msg)

        # 判断邮箱是否重复
        user = User.objects.filter(email=email)
        if user:
            msg['code'] = 20007
            msg['msg'] = '该邮箱已被使用'
            return Response(msg)

        # 通过Serializer 注册账号
        user = UserSerializer(data=request.data)

        # 如果通过校验
        if user.is_valid():
            user.save()
        else:
            msg['code'] = 20008
            msg['msg'] = '注册资料错误请修改'
            return msg

        # 注册后跳转到首页
        msg['url'] = reverse('user:login')
        # 修改密码
        user_obj = User.objects.filter(username=username).first()
        user_obj.password = encrypt_md5(password)
        user_obj.save()
        # 异步发送邮件
        send_register_active_email.delay(email, username, str(encrypt_pk(user_obj.pk)))

        # 记录日志
        # log.error('注册账户:%s 邮件已发送' % username)
        return Response(msg)


# 自动创建用户详情表
@receiver(post_save, sender=User)
def create_user_details(sender, **kwargs):
    if kwargs.get('created', False):
        user_pk = kwargs.get('instance').pk  # 注册用户的ID
        try:
            user_details_obj = User_Details.objects.create(user_id=user_pk)
            user_details_obj.shop_link = 'shop/shop/' + str(encrypt_pk(user_pk))
            user_details_obj.save()
        except:
            pass


# 邮箱
class Active_View(APIView):
    def get(self, request, pk):
        try:
            user_pk = deciphering_pk(int(pk))
            user_info = User.objects.filter(pk=user_pk).first()
            user_info.account_type = 0
            user_info.save()
            return redirect('user:login')
        except:
            return HttpResponse('激活链接已经过期')


# 登陆
class Login_View(APIView):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        msg = {'code': 200, 'msg': ''}
        # 接收数据
        user_info = request.data
        username = user_info.get('username')
        password = user_info.get('password')

        # 校验数据
        if not all([username, password]):
            msg['code'] = 20001
            msg['msg'] = '数据不完整'
            return Response(msg)

        # 登陆校验
        user_obj = User.objects.filter(username=username, password=encrypt_md5(password)).first()
        if not user_obj:
            msg['code'] = 20001
            msg['msg'] = '用户名或者密码错误'
            return Response(msg)

        if user_obj.account_type == 1:
            msg['code'] = 20002
            msg['msg'] = '账号未激活'
            return Response(msg)

        # token加密逻辑是加密用户名
        token = encrypt_md5(username)
        # 加入缓存
        cache.set(token, user_obj.pk, 3600)

        # 添加登陆记录
        ip = request.META.get('REMOTE_ADDR')
        time_obj = Login_log.objects.create(login_addr=ip, user_id=user_obj.pk)

        # 切割登陆时间utc时间,创建出来的对象是少八小时的，数据库里面会加八小时
        last_landing_time = time_obj.login_time
        # print('创建对象的时间:',time_obj.login_time)

        time = str(last_landing_time).split('.')[0]
        # print('要存入数据库的时间:', time)
        user_Details_obj = User_Details.objects.filter(user_id=user_obj.pk).first()
        user_Details_obj.last_landing_time = time
        user_Details_obj.last_login_addr = ip
        user_Details_obj.save()

        # 返回给前端的信息
        msg['url'] = reverse('shop:shop_index')

        # 前端的全局token
        msg['token'] = 'token=' + str(token) + ';path=/'

        return Response(msg)


# 修改密码
class Security(APIView):
    authentication_classes = [User_Authentication, ]

    def get(self, request):
        return render(request, 'user_security.html')

    def put(self, request):
        msg = {'code': 200, 'msg': '修改成功'}

        old_password = request.data.get('old_password')
        password = request.data.get('password')
        affirm_password = request.data.get('affirm_password')

        # 判断三项密码是否都传递
        if not (old_password and password and affirm_password):
            msg['code'] = 201
            msg['msg'] = '不可以为空'
            return Response(msg)

        # 判断俩次密码输入是否一致
        if not (password == affirm_password):
            msg['code'] = 203
            msg['msg'] = '两次密码输入不一致'
            return Response(msg)

        # 判断密码长度与合法性
        if not (len(password) >= 6 and password.isalnum()):
            msg['code'] = 202
            msg['msg'] = '密码不能小于六位且必须是数字字母组成'
            return Response(msg)

        # 判断旧密码与数据库是否相同
        md5_password = encrypt_md5(old_password)

        # 根据加密的密码拿到用户
        user_obj = User.objects.filter(password=md5_password, username=request.user)

        # 判断用户是否存在
        if not user_obj:
            msg['code'] = 204
            msg['msg'] = '旧密码错误'
            return Response(msg)

        # 修改数据库数据
        password = encrypt_md5(affirm_password)
        user_obj.update(password=password)

        return Response(msg)


# 申请提现
class Pay_Apply(APIView):
    authentication_classes = [User_Authentication, ]

    def get(self, request):
        # 拿到当前用户的对象
        user_obj = User.objects.filter(username=request.user).first()
        user_details_obj = User_Details.objects.filter(user_id=user_obj.pk).first()
        return render(request, 'user_pay_apply.html', locals())

    def post(self, request):
        user_obj = User.objects.filter(username=request.user).first()
        user_details_obj = User_Details.objects.filter(user_id=user_obj.pk).first()
        price = request.data.get('price')
        msg = {'code': 200, 'msg': '提现申请提交成功'}
        try:
            float(price)
        except:
            msg['msg'] = '价格格式错误'
            return Response(msg)

        # 判断价格是否大于余额
        if float(price) > user_details_obj.available_balance:
            msg['msg'] = '提现金额大于余额'
            return Response(msg)

        # 修改用户信息的提现金额
        # 用户当前的提现金额
        withdraw_balance = user_details_obj.withdraw_balance
        user_details_obj.withdraw_balance = float(withdraw_balance) + float(price)
        # 修改可用余额
        user_details_obj.available_balance = float(user_details_obj.available_balance) - float(price)
        # 保存信息
        user_details_obj.save()

        # 创建提现记录
        Withdrawals_details.objects.create(amount=float(price), user_id=user_obj.pk, status_type=0)

        return Response(msg)


# 提现列表
class Pay_List(APIView):
    authentication_classes = [User_Authentication, ]

    def get(self, request):
        # 拿到用户的信息
        user_obj = User.objects.filter(username=request.user).first()
        withdrawals_details_obj = Withdrawals_details.objects.filter(user_id=user_obj.pk).all()
        return render(request, 'pay_list.html', locals())
