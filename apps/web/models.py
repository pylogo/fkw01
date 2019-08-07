from django.db import models
from tinymce.models import HTMLField


# 网站数据
class Website_data(models.Model):
    turnover = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='网站总成交额')
    profit = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='网站利润')

    class Meta:
        verbose_name_plural = '网站数据'


# # 首页设置
# class Home_settings(models.Model):
#     about = HTMLField(verbose_name='网站关于')
#     help_center = HTMLField(verbose_name='帮助中心')
#
#     class Meta:
#         verbose_name_plural = '首页设置'


# 关于
class About(models.Model):
    about_title = models.CharField(max_length=255, verbose_name='关于标题')
    about_center = models.TextField(verbose_name='关于内容')

    class Meta:
        verbose_name_plural = '关于设置'


# 帮助
class Help(models.Model):
    help_title = models.CharField(max_length=255, verbose_name='帮助标题')
    help_center = models.TextField(verbose_name='帮助内容')

    class Meta:
        verbose_name_plural = '帮助设置'


# 公告
class Affiche(models.Model):
    # user = models.ForeignKey(to='user.User', verbose_name='接收公告用户', null=True,blank=True)
    affich_title = models.TextField(verbose_name='公告标题')
    affiche_content = models.TextField(verbose_name='公告信息')
    time = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    # readig_number = models.BigIntegerField(verbose_name='阅读人数', null=True, blank=True)

    All_Affiche = (
        (0, '个人'),
        (1, '全部'),
    )
    Affiche_type = models.SmallIntegerField(choices=All_Affiche, default=0, verbose_name='全部公告')

    class Meta:
        verbose_name_plural = '公告设置'


# 网站访问量
class Visitor_Num(models.Model):
    visitor_num = models.IntegerField(default=0, verbose_name='网站访问量')
    time = models.DateTimeField(auto_now_add=True, verbose_name='访问时间')

    class Meta:
        verbose_name_plural = '网站访问量'
