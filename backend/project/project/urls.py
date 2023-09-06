import django.conf.urls.static
from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path(
        'api/v1/token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair',
    ),
    path(
        'api/v1/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh',
    ),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/v1/', include('users.urls_api')),
    path('api/v1/', include('chat.urls_api')),
    path('admin/', admin.site.urls),
]

urlpatterns += django.conf.urls.static.static(
    django.conf.settings.MEDIA_URL,
    document_root=django.conf.settings.MEDIA_ROOT,
)
