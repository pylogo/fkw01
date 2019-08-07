from django.conf.urls import url
from django.contrib import admin
from apps.shop.views import Index, Info, Link, Login_logs, Category, Commodity, Commodity_List, Commodity_Add, \
    Card_list, Shop_web, Shop_Name_Info, Order_list, Record, Alipay

urlpatterns = [
    url(r'index/', Index.as_view(), name='shop_index'),  # 主页
    url(r'info/', Info.as_view(), name='info'),  # 修改密码
    url(r'link/', Link.as_view(), name='link'),  # 店铺链接
    url(r'login/', Login_logs.as_view(), name='login'),  # 店铺链接
    url(r'category/', Category.as_view(), name='category'),  # 店铺链接
    url(r'^commodity/add', Commodity.as_view(), name='commodity'),  # 添加商品
    url(r'^commodity/list', Commodity_List.as_view(), name='commodity'),  # 商品列表
    url(r'^card/add', Commodity_Add.as_view(), name='commodity'),  # 添加卡密
    url(r'^card/list', Card_list.as_view(), name='commodity'),  # 卡密列表
    url(r'shop/(?P<pk>.*?)$', Shop_web.as_view(), name='shop_link'),  # 店铺页面
    url(r'^name/info', Shop_Name_Info.as_view(), name='Shop_Name_Info'),  # 获取商品信息
    url(r'^order/list', Order_list.as_view(), name='Shop_Name_Info'),  # 获取订单记录
    url(r'record/', Record.as_view(), name='record'),  # 查询订单
    url(r'alipay/', Alipay.as_view(), name='pay_apply'),  # 提现记录
]
