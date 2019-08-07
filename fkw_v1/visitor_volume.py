from django.core.cache import cache


class StatFlowMiddleware(object):
    """ 流量统计 """

    def __init__(self, get_response):
        self.get_response = get_response
        self.count = {}

    def __call__(self, request):
        response = self.get_response(request)
        if not cache.get('StatFlow'):
            cache.set('StatFlow', 1, 999999)
        else:
            num = cache.get('StatFlow')
            cache.set('StatFlow', num + 1, 999999)
        return response
