from rest_framework.authentication import BaseAuthentication
from apps.user.models import User
from rest_framework.exceptions import AuthenticationFailed
from django.core.cache import cache


class User_Authentication(BaseAuthentication):
    def authenticate(self, request, *args, **kwargs):
        # 获取前端带来的cookie
        token = request.COOKIES.get('token')
        pk = cache.get(token)
        user_obj = User.objects.filter(pk=pk).first()
        if user_obj:
            # 更新redis token时间
            cache.set(token, pk, 3600)
            return user_obj.username, user_obj
        else:
            msg = {'code': 40001, 'msg': '你没有登陆'}
            raise AuthenticationFailed(msg)
