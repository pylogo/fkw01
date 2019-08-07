import xadmin

from .models import *


# 卡密内容
class CardXadmin(object):
    list_display = ['id', 'card', 'card_type', 'commodity_info', 'order_record']
    search_fields = ["card", 'card_type']  # 设置搜索
    list_filter = ["card", 'card_type']  # 搜索过滤器


# 分类管理内容
class Shop_sortXadmin(object):
    list_display = ['id', 'sort_name', 'remark', 'user']
    search_fields = ['id', 'sort_name', 'remark', 'user']  # 设置搜索
    list_filter = ['id', 'sort_name', 'remark', 'user']  # 搜索过滤器


# 商品信息内容
class Commodity_InfoXadmin(object):
    list_display = ['id', 'shop_name', 'sold_type', 'price', 'remaining_stock', 'describe', 'shop_sort', 'sold']
    search_fields = ['id', 'shop_name', 'sold_type', 'price', 'remaining_stock', 'describe', 'shop_sort',
                     'sold']  # 设置搜索
    list_filter = ['id', 'shop_name', 'sold_type', 'price', 'remaining_stock', 'describe', 'shop_sort', 'sold']  # 搜索过滤器


# 订单记录
class Order_recordXadmin(object):
    list_display = ['id', 'order_number', 'order_status_type', 'create_time', 'pay_time', 'payment_method', 'num',
                    'amount', 'account_entry', 'buyer_email', 'trade_no', 'card_info', 'commodity_info', 'user',
                    'shop_cell','total_balance']
    search_fields = ['id', 'order_number', 'order_status_type', 'create_time', 'pay_time', 'payment_method', 'num',
                     'amount', 'account_entry', 'buyer_email', 'trade_no', 'card_info', 'commodity_info', 'user',
                     'shop_cell']  # 设置搜索
    list_filter = ['id', 'order_number', 'order_status_type', 'create_time', 'pay_time', 'payment_method', 'num',
                   'amount', 'account_entry', 'buyer_email', 'trade_no', 'card_info', 'commodity_info', 'user',
                   'shop_cell']  # 搜索过滤器

    data_charts = {
        "order_amount": {'title': '订单金额', "x-field": "id", "y-field": ('total_balance',),
                         "order": ('id',)},
        # "order_count": {'title': '订单量', "x-field": "create_time", "y-field": ('amount',),
        #                 "order": ('create_time',)},
    }


#
# class Order_recordAdmin(object):
#     data_chats = {
#         "order_amount": {'title': '订单金额', "x-field": "create_time", "y-field": ('amount',),
#                          "order": ('create_time',)},
#         # "order_count": {'title': '订单量', "x-field": "create_time", "y-field": ('total_count',),
#         #                 "order": ('create_time',)},
#     }


xadmin.site.register(Card, CardXadmin)
xadmin.site.register(Shop_sort, Shop_sortXadmin)
xadmin.site.register(Commodity_Info, Commodity_InfoXadmin)
xadmin.site.register(Order_record, Order_recordXadmin)
