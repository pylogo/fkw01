from django.conf.urls import url
from django.contrib import admin
from .views import Register, Active_View, Login_View, Security, Pay_Apply, Pay_List

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^register/', Register.as_view(), name='register'),  # 注册
    url(r'login/', Login_View.as_view(), name='login'),  # 登陆
    url(r'active/(?P<pk>.*?)$', Active_View.as_view(), name='active'),  # 激活
    url(r'security/', Security.as_view(), name='security'),  # 修改密码
    url(r'pay/apply/', Pay_Apply.as_view(), name='pay_apply'),  # 申请提现
    url(r'pay/list/', Pay_List.as_view(), name='pay_apply'),  # 提现记录

]
