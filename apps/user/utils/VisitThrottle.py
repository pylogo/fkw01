from rest_framework.throttling import SimpleRateThrottle


class VisitThrottle(SimpleRateThrottle):
    scope = 'fkw_user'

    def get_cache_key(self, request, view):
        return request.META.get('REMOTE_ADDR')
