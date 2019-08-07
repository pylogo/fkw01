from django.db import models


# 用户的基本信息
class User(models.Model):
    username = models.CharField(max_length=255, verbose_name='用户名')
    password = models.CharField(max_length=255, verbose_name='密码')
    email = models.EmailField(verbose_name='邮箱')
    qq = models.CharField(max_length=255, verbose_name='QQ', blank=True, null=True)
    account_choices = (
        (0, '激活'),
        (1, '未激活'),
        (2, '禁用'),
    )
    account_type = models.SmallIntegerField(choices=account_choices, default=1, verbose_name='账号激活状态')
    User_choices = (
        (0, '商户'),
        (1, '管理员'),
    )
    User_type = models.SmallIntegerField(choices=User_choices, default=0, verbose_name='账户类型')
    creation_time = models.DateField(auto_now_add=True, verbose_name='创建时间', null=True, blank=True)

    class Meta:
        verbose_name_plural = '用户表'

    def __str__(self):
        return self.username


# 商户的详情
class User_Details(models.Model):
    user = models.OneToOneField(to='User', blank=True, null=True)
    available_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='可用余额')
    total_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='总收益')
    withdraw_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='提现余额')
    transactions_Number = models.CharField(max_length=255, default=0, verbose_name='成交次数')
    shop_link = models.CharField(verbose_name='店铺地址', max_length=255, blank=True, null=True)
    shop_name = models.CharField(max_length=255, verbose_name='店铺名称', blank=True, null=True)
    shop_announcement = models.CharField(max_length=255, verbose_name='店铺公告', blank=True, null=True, default='此人很懒没有公告')
    shop_account = models.CharField(max_length=255, verbose_name='收款账户', blank=True, null=True)
    handling_fee = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='手续费比例', default=5)
    last_landing_time = models.CharField(max_length=255, verbose_name='最后登陆时间', blank=True, null=True)
    last_login_addr = models.CharField(max_length=255, verbose_name='登陆的ip地址', blank=True, null=True)

    class Meta:
        verbose_name_plural = '商户详情'

    def __str__(self):
        return self.user.username


# 提现详情
class Withdrawals_details(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='金额')
    handling_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='手续费')
    handling_fee_status = (
        (0, '提现成功'),
        (1, '未处理'),
        (2, '提现失败'),
    )
    status_type = models.SmallIntegerField(choices=handling_fee_status, default=1, verbose_name='提现状态')
    creation_time = models.DateField(auto_now_add=True, verbose_name='创建时间')
    pay_time = models.DateField(null=True, verbose_name='打款时间')
    user = models.ForeignKey(to='User', verbose_name='商户ID')

    class Meta:
        verbose_name_plural = '提现记录'


# 登陆日志
class Login_log(models.Model):
    login_time = models.DateTimeField(auto_now_add=True, verbose_name='登陆时间')
    login_addr = models.CharField(max_length=255, verbose_name='登陆ip')
    user = models.ForeignKey(to='User', verbose_name='商户ID')

    class Meta:
        verbose_name_plural = '登陆日志'

    def __str__(self):
        return self.user.username
