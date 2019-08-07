from django.shortcuts import render, redirect
from rest_framework.views import APIView, Response
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from apps.web.models import About, Help


# 首页
@method_decorator(cache_page(60 * 60), name='dispatch')
class Index(APIView):
    def get(self, request):
        return render(request, 'index.html')


# 关于
class About1(APIView):
    def get(self, request):
        ablot_obj = About.objects.filter(id=1).first()
        return render(request, 'about.html', locals())


# 帮助
class Help1(APIView):
    def get(self, request):
        help_obj = Help.objects.filter(id=1).first()
        return render(request, 'help.html', locals())
