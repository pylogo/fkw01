from django.db import models


# 商品分类
class Shop_sort(models.Model):
    sort_name = models.CharField(max_length=255, verbose_name='分类名称')
    remark = models.CharField(max_length=255, verbose_name='分类备注', default='')
    user = models.ForeignKey(to='user.User', verbose_name='用户ID')

    class Meta:
        verbose_name_plural = '商品分类'

    def __str__(self):
        return self.sort_name


# 商品信息
class Commodity_Info(models.Model):
    shop_name = models.CharField(max_length=255, verbose_name='商品名称')
    sold_status = (
        (0, '上架'),
        (1, '未上架'),
        (2, '异常'),
    )
    sold_type = models.SmallIntegerField(choices=sold_status, default=1, verbose_name='销售状态')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='商品价格')
    remaining_stock = models.IntegerField(default=0, verbose_name='剩余库存')
    describe = models.CharField(max_length=255, default='', verbose_name='商品描述')
    shop_sort = models.ForeignKey(to='Shop_sort', verbose_name='分类')
    user_id = models.CharField(max_length=255, verbose_name='商户ID', default='')
    sold = models.CharField(max_length=255, verbose_name='已售', default=0)

    class Meta:
        verbose_name_plural = '商品信息'

    def __str__(self):
        return self.shop_name


# 卡密
class Card(models.Model):
    card = models.CharField(max_length=255, verbose_name='卡密内容')
    card_status = (
        (0, '使用'),
        (1, '未使用'),
    )
    card_type = models.SmallIntegerField(choices=card_status, default=1, verbose_name='卡密状态')
    commodity_info = models.ForeignKey(to='Commodity_Info', verbose_name='商品ID')
    user_id = models.CharField(max_length=255, verbose_name='商户ID', default='')
    order_record = models.ForeignKey(to='Order_record', verbose_name='订单ID', null=True, blank=True)

    class Meta:
        verbose_name_plural = '卡密'

    def __str__(self):
        return self.card


# 订单记录
class Order_record(models.Model):
    order_number = models.CharField(max_length=255, verbose_name='订单号')
    order_status = (
        (0, '付款'),
        (1, '未付款'),
        (2, '关闭'),
    )
    order_status_type = models.SmallIntegerField(choices=order_status, default=1, verbose_name='订单状态')
    create_time = models.DateField(auto_now_add=True, verbose_name='创建订单时间')
    pay_time = models.CharField(max_length=255, verbose_name='支付时间', null=True, blank=True)
    payment_method_choices = (
        (0, '支付宝'),
        (1, '微信'),
    )
    payment_method = models.SmallIntegerField(choices=payment_method_choices, default=0, verbose_name='支付方式')
    num = models.CharField(max_length=255, verbose_name='数量', default=0)
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='金额')
    account_entry = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='平台利润')
    buyer_email = models.CharField(max_length=255, null=True, verbose_name='买家邮箱', blank=True)
    trade_no = models.CharField(max_length=255, verbose_name='支付编号', null=True, blank=True)
    card_info = models.TextField(verbose_name='卡密内容', null=True, blank=True)
    commodity_info = models.ForeignKey(to='Commodity_Info', verbose_name='商品ID')
    user = models.ForeignKey(to='user.User', verbose_name='用户ID')
    shop_cell = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='商户入账', default=0)
    total_balance = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='网站总收益', default=0)

    class Meta:
        verbose_name_plural = '订单记录'

    def __str__(self):
        return self.order_number
