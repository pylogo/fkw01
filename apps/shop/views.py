from django.shortcuts import render
from rest_framework.views import APIView
from apps.user.models import User, User_Details, Login_log
from apps.user.interface.User_Auth import User_Authentication
from rest_framework.response import Response
from fkw_v1.settings import REALM_NAME
from apps.shop.models import Shop_sort, Commodity_Info, Card, Order_record
from django.core.cache import cache
from apps.user.interface.shop_link_password import encrypt_pk, deciphering_pk
from apps.shop.interface.shop_order_number import shop_order
from datetime import datetime
from django.db.models import F
from apps.web.models import Website_data
from celery_task.user_task import send_km_active_email
from django.shortcuts import render, redirect, HttpResponse
from fkw_v1 import settings
from myutils.pay import AliPay
from apps.web.models import Affiche
import json
import time


def ali():
    alipay = AliPay(
        appid=settings.app_id,
        app_notify_url=settings.notify_url,
        return_url=settings.return_url,
        app_private_key_path=settings.merchant_private_key_path,
        alipay_public_key_path=settings.alipay_public_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥
        debug=True,  # 默认False,
    )
    return alipay


# 店铺主页
class Index(APIView):
    authentication_classes = [User_Authentication, ]

    def get(self, request):
        user = request.user
        user_info = User.objects.filter(username=user).first()
        affiche = Affiche.objects.all()

        # print(user_info)
        return render(request, 'shop_index.html', locals())


# 店铺信息
class Info(APIView):
    authentication_classes = [User_Authentication, ]

    def get(self, request):
        user = request.user
        user_info = User.objects.filter(username=user).first()
        return render(request, 'shop_info.html', locals())

    def put(self, request):
        msg = {'code': 200, 'msg': '修改成功'}
        shop_id = request.data.get('shop_id')
        shop_email = request.data.get('shop_email')
        shop_qq = request.data.get('shop_qq')
        shop_name = request.data.get('shop_name')
        shop_announcement = request.data.get('shop_announcement')
        shop_account = request.data.get('shop_account')

        if not (shop_qq and shop_name and shop_announcement and shop_account):
            msg['code'] = 20001
            msg['msg'] = '信息不完整'
            return Response(msg)

        elif not ((shop_qq != 'None') and (shop_name != 'None') and (shop_announcement != 'None') and (
                shop_account != 'None')):
            msg['code'] = 20001
            msg['msg'] = '信息不完整'
            return Response(msg)

        else:
            # 保存qq
            user = User.objects.filter(pk=int(shop_id)).first()
            user.qq = shop_qq
            user.save()

            # 保存店铺信息
            shop_info = User_Details.objects.filter(user_id=user.pk)
            if not shop_info:
                User_Details.objects.create(user_id=user.pk, shop_name=shop_name,
                                            shop_announcement=shop_announcement, shop_account=shop_account)
            else:
                shop_info.update(shop_name=shop_name, shop_announcement=shop_announcement, shop_account=shop_account)

            return Response(msg)


# 店铺链接
class Link(APIView):
    authentication_classes = [User_Authentication, ]

    def get(self, request):
        # 判断用户是否有店铺链接
        user = request.user
        user_info = User.objects.filter(username=user).first()
        shop_details_info = User_Details.objects.filter(user_id=user_info.pk).first()

        link = REALM_NAME + shop_details_info.shop_link
        # print(link)
        return render(request, 'shop_link.html', locals())


# 登陆日志
class Login_logs(APIView):
    authentication_classes = [User_Authentication, ]

    def get(self, request):
        user_info = User.objects.filter(username=request.user).first()
        login_obj = Login_log.objects.filter(user_id=user_info.pk).all()
        return render(request, 'login_log.html', locals())


# 商品分类
class Category(APIView):
    authentication_classes = [User_Authentication, ]

    def get(self, request):
        user_info = User.objects.filter(username=request.user).first()
        all_category = Shop_sort.objects.filter(user_id=user_info.pk)
        return render(request, 'shop_category.html', locals())

    def post(self, request):
        msg = {'code': 200, 'msg': '添加成功'}

        # 登陆用户信息
        user_info = User.objects.filter(username=request.user).first()
        add_category_name = request.data.get('add_category_name')
        add_category_remark = request.data.get('add_category_remark')

        # 分类不可以为空
        if not add_category_name:
            msg['code'] = 201
            msg['msg'] = '分类名不可以为空'
            return Response(msg)

        # 判断分类是否存在
        shop_sort_obj = Shop_sort.objects.filter(sort_name=add_category_name)
        if shop_sort_obj:
            msg['code'] = 202
            msg['msg'] = '分类名已存在'
            return Response(msg)

        # 创建分类
        shop_sort_obj = Shop_sort.objects.create(sort_name=add_category_name, remark=add_category_remark,
                                                 user_id=user_info.pk)

        if not shop_sort_obj:
            msg['code'] = 203
            msg['msg'] = '分类创建失败'
            return Response(msg)
        else:
            msg['url'] = '/shop/category/'
            return Response(msg)

    def delete(self, request):
        msg = {'code': 200, 'msg': '添加成功'}
        delete_id = request.data.get('pk')
        Shop_sort.objects.filter(id=delete_id).delete()
        msg['url'] = '/shop/category/'

        return Response(msg)


# 添加商品
class Commodity(APIView):
    authentication_classes = [User_Authentication, ]

    def get(self, request):
        # 拿到登陆的用户ID
        user = request.user
        user_info = User.objects.filter(username=user).first()
        # 通过ID拿到分类
        sort_obj = Shop_sort.objects.filter(user_id=user_info.pk)
        # print(sort_obj)
        return render(request, 'add_commodity.html', locals())

    def post(self, request):
        msg = {'code': 200, 'msg': '添加成功'}
        # 拿到登陆的用户ID
        user_info = User.objects.filter(username=request.user).first()
        # 前端发来的信息
        sort_id = request.data.get('sort_id')
        shop_name = request.data.get('shop_name')
        shop_price = request.data.get('shop_price')
        shop_describe = request.data.get('shop_describe')
        shop_status = request.data.get('shop_status')

        # 判断名称价格是否为空
        if not (shop_name and shop_price):
            msg['code'] = 201
            msg['msg'] = '名称价格不可以为空'
            return Response(msg)

        # 判断价格格式是否正确
        try:
            shop_price = float(shop_price)
        except:
            msg['code'] = 202
            msg['msg'] = '价格格式错误'
            return Response(msg)

        # 根据分类名称拿到的ID
        sort_obj = Shop_sort.objects.filter(sort_name=sort_id).first()

        # 判断商品名称是否存在
        commodity_info_obj = Commodity_Info.objects.filter(shop_name=shop_name).first()
        if commodity_info_obj:
            msg['msg'] = '商品已存在'
            return Response(msg)

        # 判断上架下架
        sun = 0
        if shop_status == '下架':
            sun = 1
        # 创建对象
        commodity_info = Commodity_Info.objects.create(shop_name=shop_name, sold_type=sun, price=shop_price,
                                                       shop_sort_id=sort_obj.pk, describe=shop_describe,
                                                       user_id=user_info.pk)
        if commodity_info:
            msg['url'] = '/shop/commodity/list'
            return Response(msg)
        else:
            msg['msg'] = '添加失败'
            return Response(msg)


# 商品列表
class Commodity_List(APIView):
    authentication_classes = [User_Authentication, ]

    def get(self, request):
        # 拿到当前登陆用户的所有商品
        # 拿到登陆的用户ID
        user = request.user
        user_info = User.objects.filter(username=user).first()

        # 拿到所有商品
        all_shop = Commodity_Info.objects.filter(user_id=user_info.pk)
        return render(request, 'shop_list.html', locals())

    def delete(self, request):
        msg = {'code': 200, 'msg': '删除成功'}
        pk = request.data.get('pk')
        Commodity_Info.objects.filter(pk=pk).delete()
        msg['url'] = '/shop/commodity/list'
        return Response(msg)

    def put(self, request):
        msg = {'code': 200, 'msg': '修改状态成功', 'url': '/shop/commodity/list'}

        # 拿到前端发来的信息
        pk = request.data.get('pk')
        status = request.data.get('status')

        # 判断status
        commodity_info_obj = Commodity_Info.objects.filter(pk=pk)
        if status == 'down':
            # 下架
            commodity_info_obj.update(sold_type=1)
        else:
            commodity_info_obj.update(sold_type=0)

        return Response(msg)


# 添加卡密
class Commodity_Add(APIView):
    authentication_classes = [User_Authentication, ]

    def get(self, request):
        user = request.user
        user_info = User.objects.filter(username=user).first()

        # 拿到所有商品
        all_shop = Commodity_Info.objects.filter(user_id=user_info.pk)
        return render(request, 'add_card.html', locals())

    def post(self, request):
        user = request.user
        user_info = User.objects.filter(username=user).first()
        msg = {'code': 200, 'msg': '添加成功'}

        # 获取商品ID
        shop_name = request.data.get('sort_id')
        commodity_info_obj = Commodity_Info.objects.filter(shop_name=shop_name).first()
        shop_id = commodity_info_obj.pk

        # 获取卡密
        message_text = request.data.get('message_text')

        # 判断是否有值
        if not message_text:
            msg['code'] = 201
            msg['msg'] = '卡密不可以为空'
            return Response(msg)

        # 切分卡密
        text = message_text.split('\n')

        newtext = []
        # 判断卡密长度
        for len_cord in text:
            if not len_cord:
                del len_cord
            elif len(len_cord) > 100:
                msg['code'] = 204
                msg['msg'] = '卡密长度超过限制'
                return Response(msg)
            else:
                newtext.append(len_cord)
        # 卡密个数
        count = len(newtext)

        # 批量添加卡密
        cord_list = []
        for cord in newtext:
            cord_list.append(Card(card=cord, commodity_info_id=shop_id, user_id=user_info.pk))
        if cord_list:
            Card.objects.bulk_create(cord_list)
        else:
            msg['msg'] = '异常错误,联系管理员'
            return Response(msg)

        # 从缓存中拿到当前卡密量
        if not cache.get('shop_cord_id' + str(shop_id)):
            # 拿到当前数据库所有数据
            all_cord = Card.objects.filter(commodity_info_id=shop_id, card_type=1).all()
            cache.set('shop_cord_id' + str(shop_id), len(all_cord), 60 * 60 * 24)
        else:
            # 修改缓存数据库
            # 当前缓存数据库总量
            count1 = cache.get('shop_cord_id' + str(shop_id))
            # 修改缓存数据库总量
            cache.set('shop_cord_id' + str(shop_id), count1 + count, 60 * 60 * 24)

        # 修改商品库存
        commodity_info_obj.remaining_stock = cache.get('shop_cord_id' + str(shop_id))
        commodity_info_obj.save()

        # 提示信息
        msg['url'] = '/shop/commodity/list'
        msg['msg'] = '成功添加卡密:%s条' % count

        return Response(msg)


# 查看所有卡密
class Card_list(APIView):
    authentication_classes = [User_Authentication, ]

    def get(self, request):
        user_info = User.objects.filter(username=request.user).first()
        card_all_info = Card.objects.filter(user_id=user_info.pk).all()
        # # 拿到当前用户的所有卡密
        return render(request, 'card_list.html', locals())
        # ret = card_all_info
        # # 实例化产生一个偏移分页对象
        # page = CursorPagination()
        # # 三个参数：
        # # 每页显示的大小
        # page.page_size = 3
        # # 查询的key值
        # page.cursor_query_param = 'cursor'
        # # 按什么排序
        # page.ordering = 'id'
        #
        # ret_page = page.paginate_queryset(ret, request, self)
        # # 序列化
        # pub_ser = CardSerializers(ret_page, many=True)
        # # 去setting中配置每页显示多少条
        # return page.get_paginated_response(pub_ser.data)

    def delete(self, request):
        msg = {'code': 200, 'msg': '删除成功'}
        pk = request.data.get('pk')  # 要删除对象的pk值
        Card_obj = Card.objects.filter(pk=pk).first()  # 要删除卡密的对象
        shop_name = Card_obj.commodity_info  # 要删除对象所属的商品名
        commodity_info = Commodity_Info.objects.filter(shop_name=shop_name).first()  # 要删除对象的商品对象
        remaining_stock = commodity_info.remaining_stock  # 拿到当前商品的库存
        Card_obj.delete()  # 删除要卡密数据
        remaining_stock = int(remaining_stock) - 1  # 删除后的库存量
        commodity_info.remaining_stock = remaining_stock  # 修改库存
        commodity_info.save()  # 保存数据
        # 跳转卡密列表
        msg['url'] = '/shop/card/list'

        # 修改缓存数据库总量
        count1 = cache.get('shop_cord_id' + str(commodity_info.pk))  # 当前的库存量
        cache.set('shop_cord_id' + str(commodity_info.pk), int(count1) - 1, 60 * 60 * 24)  # 更新缓存库存

        return Response(msg)


# 商家店铺页面
class Shop_web(APIView):

    def get(self, request, pk):
        # 解密数据
        try:
            pk = deciphering_pk(pk)
            user_info = User.objects.filter(pk=pk).first()
            sort_info = Shop_sort.objects.filter(user_id=user_info.pk)
            return render(request, 'shop.html', locals())
        except:
            return Response('店铺不存在')

    def post(self, request, pk):
        # 拿到当前用户所有的分类名称

        pk = deciphering_pk(pk)
        user_info = User.objects.filter(pk=pk).first()
        sort_info = Shop_sort.objects.filter(user_id=user_info.pk, commodity_info__sold_type=0).values_list('sort_name',
                                                                                                            'commodity_info__shop_name')
        sort_func_dic = {}
        commodity_func_dic = {}

        for number, sort_name_dic in enumerate(sort_info, 1):
            if sort_name_dic[0] in sort_func_dic:
                sort_func_dic[sort_name_dic[0]].append(sort_name_dic[1])
            else:
                sort_func_dic[sort_name_dic[0]] = [sort_name_dic[1]]

        province_list = {}
        city_list = {}
        for index, keys in enumerate(sort_func_dic.keys(), 1):
            province_list[str(index).zfill(2) + str('0000')] = keys
            for i, values in enumerate(sort_func_dic[keys], 1):
                city_list[str(index).zfill(2) + str(i).zfill(2) + str('00')] = values

        commodity_func_dic['province_list'] = province_list
        commodity_func_dic['city_list'] = city_list

        # 拿到分类下所有商品名称
        return Response({'data': commodity_func_dic})


# 获取店铺商品及价格
class Shop_Name_Info(APIView):
    def post(self, request):
        shop_name = request.data.get('shop_name')
        # 根据商品名称拿到商品的价格
        shop_info = Commodity_Info.objects.filter(shop_name=shop_name).values('price', 'remaining_stock', 'describe')
        data = shop_info[0]
        return Response(data)

    def put(self, request):
        selector = request.data.get('city-selector')  # 商品名称
        quantity = request.data.get('quantity')  # 数量
        should_pay = request.data.get('should-pay')  # 总额
        contact = request.data.get('contact')  # 联系方式

        msg = {'code': 200, 'msg': '购买成功，请查看邮箱或者短信'}
        # 先判断联系方式是否为空
        if not contact:
            msg['code'] = 201
            msg['msg'] = '联系方式不可以为空'
            return Response(msg)
        # 拿到数据商品名称的库存
        shop_info = Commodity_Info.objects.filter(shop_name=selector).values('price', 'remaining_stock',
                                                                             'user_id', 'pk')
        remaining_stock = shop_info[0].get('remaining_stock')
        price = shop_info[0].get('price')

        # 大于库存
        if int(quantity) > int(remaining_stock):
            msg['code'] = 202
            msg['msg'] = '库存不足！请减少购买量或联系作者！'
            return Response(msg)

        # 判断总额是否与数据库计算的总额相同
        sql_price = float(quantity) * float(price)
        if round(float(sql_price), 2) != float(should_pay):
            msg['code'] = 203
            msg['msg'] = '非法金额'
            return Response(msg)

        # 生成订单
        order_number = shop_order()  # 订单号
        num = quantity  # 购买数量
        amount = round(float(sql_price), 2)  # 金额
        account_entry = amount * 0.05  # 平台利润
        buyer_email = contact  # 买家联系方式
        commodity_info_id = shop_info[0].get('pk')  # 商品ID
        user_id = shop_info[0].get('user_id')  # 商户ID
        shop_cell = amount - account_entry  # 商户入账

        # 创建订单记录
        order_record_obj = Order_record.objects.create(order_number=order_number, num=num, amount=amount,
                                                       account_entry=account_entry, buyer_email=buyer_email,
                                                       commodity_info_id=commodity_info_id, user_id=user_id)

        alipay = ali()
        # 生成支付的url
        # 对象调用direct_pay
        # 该方法生成一个加密串
        query_params = alipay.direct_pay(
            subject="测试商品",  # 商品简单描述
            out_trade_no=order_number,  # 商户订单号
            total_amount=amount,  # 交易金额(单位: 元 保留俩位小数)
        )

        pay_url = "https://openapi.alipaydev.com/gateway.do?{}".format(query_params)
        # print(pay_url)
        # 朝这个地址发get
        #
        # 请求
        # from django.http import JsonResponse
        # return JsonResponse({'status':100,'url':pay_url})
        msg = {'code': 200, 'url': pay_url}
        return Response(msg)

        # # 支付宝后台判断支付是否成功
        # res = True
        # # 如果支付成功
        # if res:
        #     order_pk = order_record_obj.pk  # 订单ID
        #     # 先从商品的卡密中拿到指定数量的卡密
        #     card_obj = Card.objects.filter(commodity_info_id=int(commodity_info_id), card_type=1).all()[:int(num)]
        #     # 修改redis卡密数量
        #     number = cache.get('shop_cord_id' + str(commodity_info_id))
        #     cache.set('shop_cord_id' + str(commodity_info_id), int(number) - int(num), 60 * 60 * 24)
        #     # 修改
        #     for i in card_obj:
        #         i.card_type = 0
        #         i.order_record_id = order_pk
        #         i.save()
        #     # 在订单的卡密中添加指定数据且改变付款状态
        #     # 支付时间格式
        #     time = str(datetime.now()).split('.')[0]
        #     card_list = [i.card for i in card_obj]
        #     Order_record.objects.filter(id=order_pk).update(card_info=card_list, order_status_type=0,
        #                                                     pay_time=time)  # 修改数据库
        #
        #     # 修改商品库存
        #     # print(commodity_info_id, type(commodity_info_id))
        #     Commodity_Info.objects.filter(pk=int(commodity_info_id)).update(remaining_stock=F('remaining_stock') - num,
        #                                                                     sold=F('sold') + num)
        #
        #     """
        #     指定条数的卡密且修改了拿到卡密的状态
        #     在订单记录中添加了卡密内容，修改了付款状态
        #     修改了商品的库存与销量
        #     修改了支付时间
        #     """
        #     # 支付成功修改商户入账金额
        #     # 重新查订单的pk
        #     Order_record.objects.filter(pk=order_pk).update(shop_cell=shop_cell)
        #     # 修改商户详情的可以用余额，总余额，成交次数，成交额，利润
        #     User_Details.objects.filter(user_id=user_id).update(
        #         available_balance=F('available_balance') + int(shop_cell),
        #         total_balance=F('total_balance') + int(shop_cell),
        #         transactions_Number=
        #         F('transactions_Number') + 1, )
        #     # 修改网站总成交额，网站利润
        #     Website_data.objects.filter(pk=1).update(turnover=F('turnover') + amount,
        #                                              profit=F('profit') + account_entry)
        #     # 修改订单记录中网站总销售额
        #     Website_data_obj = Website_data.objects.filter(pk=1).first()
        #     Order_record.objects.filter(pk=order_pk).update(total_balance=Website_data_obj.profit)
        #
        #     # 发送邮件给卖家
        #     info = '订单号:%s' % order_number + '\n' + '卡密内容:'
        #     # card_info = [info + i for i in card_list][0]
        #     card_info = [i + '' + '' for i in card_list]
        #     card_info = info + str(card_info)
        #     send_km_active_email.delay(buyer_email, card_info)

        # else:
        #     pass
        #
        # return Response(msg)


# 获取订单记录
class Order_list(APIView):
    authentication_classes = [User_Authentication, ]

    def get(self, request):
        user_info = User.objects.filter(username=request.user).first()
        order_info = Order_record.objects.filter(user_id=user_info.pk).all()
        return render(request, 'order_list.html', locals())


# 查询订单
class Record(APIView):
    def get(self, request):
        return render(request, 'record.html')

    def post(self, request):
        # 前端传递过来的订单号
        dingdan = request.data.get('dingdan')
        # 通过订单号拿到订单信息
        order_record_obj = Order_record.objects.filter(order_number=dingdan).first()

        msg = {'code': 200, 'msg': '查询成功'}
        if not order_record_obj:
            msg['code'] = 201
            msg['msg'] = '订单号不存在'
            return Response(msg)

        msg['msg'] = '卡密内容:' + str(order_record_obj.card_info)
        return Response(msg)


# 阿里支付
class Alipay(APIView):
    # 支付宝如果收到用户的支付,支付宝会给我的地址发一个post请求,一个get请求

    def post(self, request):
        alipay = ali()
        # 检测是否支付成功
        # 去请求体中获取所有返回的数据：状态/订单号
        from urllib.parse import parse_qs
        body_str = request.body.decode('utf-8')

        post_data = parse_qs(body_str)
        post_dict = {}
        for k, v in post_data.items():
            post_dict[k] = v[0]
        # print('转完之后的字典', post_dict)
        # 做二次验证
        sign = post_dict.pop('sign', None)
        # 通过调用alipay的verify方法去认证
        status = alipay.verify(post_dict, sign)
        out_trade_no = post_data.get('out_trade_no')  # 订单号
        # print('测试支付宝订单', out_trade_no)

        # print('POST验证', status)
        if status:
            # 修改自己订单状态
            # 通过订单号拿到订单对象
            order_record_obj = Order_record.objects.filter(order_number=out_trade_no[0]).first()
            # print('订单对象:', order_record_obj)
            order_pk = order_record_obj.pk  # 订单ID
            commodity_info_id = order_record_obj.commodity_info.pk  # 商品ID
            # print('商品ID:', commodity_info_id)
            user_id = order_record_obj.user.pk
            num = order_record_obj.num  # 购买数量
            # 先从商品的卡密中拿到指定数量的卡密
            card_obj = Card.objects.filter(commodity_info_id=int(commodity_info_id), card_type=1).all()[:int(num)]
            # 修改redis卡密数量
            number = cache.get('shop_cord_id' + str(commodity_info_id))
            cache.set('shop_cord_id' + str(commodity_info_id), int(number) - int(num), 60 * 60 * 24)
            # 修改
            for i in card_obj:
                i.card_type = 0
                i.order_record_id = order_pk
                i.save()
            # 在订单的卡密中添加指定数据且改变付款状态
            # 支付时间格式
            time = str(datetime.now()).split('.')[0]
            card_list = [i.card for i in card_obj]
            Order_record.objects.filter(id=order_pk).update(card_info=card_list, order_status_type=0,
                                                            pay_time=time)  # 修改数据库

            # 修改商品库存
            # print(commodity_info_id, type(commodity_info_id))
            Commodity_Info.objects.filter(pk=int(commodity_info_id)).update(remaining_stock=F('remaining_stock') - num,
                                                                            sold=F('sold') + num)

            """
            指定条数的卡密且修改了拿到卡密的状态
            在订单记录中添加了卡密内容，修改了付款状态
            修改了商品的库存与销量
            修改了支付时间
            """
            # 支付成功修改商户入账金额
            # 重新查订单的pk
            # 支付价格等于
            # 订单金额
            amount = order_record_obj.amount
            # 平台利润
            account_entry = order_record_obj.account_entry
            # 商户收益
            shop_cell = amount - account_entry
            # 买家邮箱
            buyer_email = order_record_obj.buyer_email
            # 修改商户入账
            Order_record.objects.filter(pk=order_pk).update(shop_cell=shop_cell)
            # 修改商户详情的可以用余额，总余额，成交次数，成交额，利润
            User_Details.objects.filter(user_id=user_id).update(
                available_balance=F('available_balance') + int(shop_cell),
                total_balance=F('total_balance') + int(shop_cell),
                transactions_Number=
                F('transactions_Number') + 1, )
            # 修改网站总成交额，网站利润
            Website_data.objects.filter(pk=1).update(turnover=F('turnover') + amount,
                                                     profit=F('profit') + account_entry)
            # 修改订单记录中网站总销售额
            Website_data_obj = Website_data.objects.filter(pk=1).first()
            Order_record.objects.filter(pk=order_pk).update(total_balance=Website_data_obj.profit)

            # 发送邮件给卖家
            info = '订单号:%s' % out_trade_no + '\n' + '卡密内容:'
            # card_info = [info + i for i in card_list][0]
            card_info = [i + '' + '' for i in card_list]
            card_info = info + str(card_info)
            send_km_active_email.delay(buyer_email, card_info)

        # 返回信息给支付宝，支付宝收到任何一个请求就不再发信息回来了，要不然会一直发
        return HttpResponse('POST返回')

    def get(self, request):
        alipay = ali()
        params = request.GET.dict()
        sign = params.pop('sign', None)
        status = alipay.verify(params, sign)
        return HttpResponse('支付成功,请查看邮箱！')
