import django.conf
import django.core.cache
import django.http


class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        key = f'ratelimit:{request.META.get("REMOTE_ADDR")}'
        count = django.core.cache.cache.get(key, 1)
        if not django.conf.settings.RATE_LIMIT_MIDDLEWARE:
            return self.get_response(request)

        if count >= django.conf.settings.REQUESTS_PER_SECOND:
            return django.http.HttpResponse('Too many requests', status=429)
        else:
            django.core.cache.cache.set(key, count + 1, 1)
            return self.get_response(request)
