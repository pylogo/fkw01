from django.conf.urls import url
from .views import Index, About1, Help1

urlpatterns = [
    url(r'^about/', About1.as_view()),
    url(r'^help', Help1.as_view()),
    url(r'', Index.as_view()),
]
