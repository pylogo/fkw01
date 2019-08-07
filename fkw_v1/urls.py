from django.conf.urls import url, include
from django.contrib import admin
import xadmin

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^tinymce/', include('tinymce.urls')),  # 富文本编辑器
    url(r'^admin/', admin.site.urls),
    url(r'^user/', include('apps.user.urls', namespace='user')),
    url(r'^shop/', include('apps.shop.urls', namespace='shop')),
    url(r'^web/', include('apps.web.urls', namespace='web')),
    url(r'', include('apps.web.urls', namespace='web')),
]
