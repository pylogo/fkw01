import xadmin

from .models import *


# 用户内容
class UserXadmin(object):
    list_display = ['id', 'username', 'email', 'qq', 'account_type', 'User_type', 'creation_time']
    search_fields = ['id', 'username', 'email', 'qq', 'account_type', 'User_type']  # 设置搜索
    list_filter = ['id', 'username', 'email', 'qq', 'account_type', 'User_type']  # 搜索过滤器
    data_charts = {
        "order_amount": {'title': '注册量', "x-field": "creation_time", "y-field": ('id',),
                         "order": ('id',)},
        # "order_count": {'title': '订单量', "x-field": "create_time", "y-field": ('amount',),
        #                 "order": ('create_time',)},
    }


# 商户详情内容
class User_DetailsXadmin(object):
    list_display = ['id', 'user', 'available_balance', 'total_balance', 'withdraw_balance', 'transactions_Number',
                    'shop_link', 'shop_name', 'shop_announcement', 'shop_account', 'handling_fee', 'last_landing_time',
                    'last_login_addr']
    search_fields = ['id', 'user', 'available_balance', 'total_balance', 'withdraw_balance', 'transactions_Number',
                     'shop_link', 'shop_name', 'shop_announcement', 'shop_account', 'handling_fee', 'last_landing_time',
                     'last_login_addr']  # 设置搜索
    list_filter = ['id', 'user', 'available_balance', 'total_balance', 'withdraw_balance', 'transactions_Number',
                   'shop_link', 'shop_name', 'shop_announcement', 'shop_account', 'handling_fee', 'last_landing_time',
                   'last_login_addr']  # 搜索过滤器


# 用户内容
class Withdrawals_detailsXadmin(object):
    list_display = ['id', 'amount', 'handling_fee', 'status_type', 'creation_time', 'pay_time', 'user']
    search_fields = ['id', 'amount', 'handling_fee', 'status_type', 'creation_time', 'pay_time', 'user']  # 设置搜索
    list_filter = ['id', 'amount', 'handling_fee', 'status_type', 'creation_time', 'pay_time', 'user']  # 搜索过滤器


# 用户内容
class Login_logXadmin(object):
    list_display = ['id', 'user', 'login_time', 'login_addr']
    search_fields = ['id', 'user', 'login_time', 'login_addr']  # 设置搜索
    list_filter = ['id', 'user', 'login_time', 'login_addr']  # 搜索过滤器


xadmin.site.register(User, UserXadmin)
xadmin.site.register(User_Details, User_DetailsXadmin)
xadmin.site.register(Withdrawals_details, Withdrawals_detailsXadmin)
xadmin.site.register(Login_log, Login_logXadmin)
