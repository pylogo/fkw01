import xadmin

from .models import *

from xadmin import views


class BaseSetting(object):
    '''
    主题样式多样化
    '''
    enable_themes = True
    use_bootswatch = True


class GlobalSetting(object):
    # 页头
    site_title = '木柯发卡网后台管理系统'
    # 页脚
    site_footer = '木柯网络游戏有限公司'
    # 左侧样式
    menu_style = 'accordion'


xadmin.site.register(views.CommAdminView, GlobalSetting)

xadmin.site.register(views.BaseAdminView, BaseSetting)


# 网站数据
class Website_dataXadmin(object):
    list_display = ['id', 'turnover', 'profit']
    search_fields = ['id', 'turnover', 'profit']  # 设置搜索
    list_filter = ['id', 'turnover', 'profit']  # 搜索过滤器


# 关于
class AboutXadmin(object):
    list_display = ['id', 'about_title', 'about_center']
    search_fields = ['id', 'about_title', 'about_center']  # 设置搜索
    list_filter = ['id', 'about_title', 'about_center']  # 搜索过滤器


# 帮助
class HelpXadmin(object):
    list_display = ['id', 'help_title', 'help_center']
    search_fields = ['id', 'help_title', 'help_center']  # 设置搜索
    list_filter = ['id', 'help_title', 'help_center']  # 搜索过滤器


# 公告数据
class AfficheXadmin(object):
    list_display = ['id', 'affich_title', 'affiche_content', 'time',  'Affiche_type']
    search_fields = ['id', 'affich_title', 'affiche_content', 'time',  'Affiche_type']  # 设置搜索
    list_filter = ['id', 'affich_title', 'affiche_content', 'time',  'Affiche_type']  # 搜索过滤器


# 网站访问量
class Visitor_NumXadmin(object):
    list_display = ['id', 'visitor_num', 'time']
    search_fields = ['id', 'visitor_num', 'time']  # 设置搜索
    list_filter = ['id', 'visitor_num', 'time']  # 搜索过滤器

    data_charts = {
        "order_amount": {'title': '访问量', "x-field": "time", "y-field": ('visitor_num',),
                         "order": ('time',)},
    }


xadmin.site.register(Website_data, Website_dataXadmin)
xadmin.site.register(About, AboutXadmin)
xadmin.site.register(Help, HelpXadmin)
xadmin.site.register(Affiche, AfficheXadmin)
xadmin.site.register(Visitor_Num, Visitor_NumXadmin)
