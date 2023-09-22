import django.conf.urls.static
import django.contrib
import django.urls
import rest_framework_simplejwt.views

urlpatterns = [
    django.urls.path(
        'api/v1/token/',
        rest_framework_simplejwt.views.TokenObtainPairView.as_view(),
        name='token_obtain_pair',
    ),
    django.urls.path(
        'api/v1/token/refresh/',
        rest_framework_simplejwt.views.TokenRefreshView.as_view(),
        name='token_refresh',
    ),
    # todo: use token verify
    django.urls.path(
        'api/v1/token/verify/',
        rest_framework_simplejwt.views.TokenVerifyView.as_view(),
        name='token_verify',
    ),
    django.urls.path('api/v1/', django.urls.include('users.urls_api')),
    django.urls.path('api/v1/', django.urls.include('chat.urls_api')),
    django.urls.path('admin/', django.contrib.admin.site.urls),
]
urlpatterns += [
    django.urls.path('api-auth/', django.urls.include('rest_framework.urls')),
]

urlpatterns += django.conf.urls.static.static(
    django.conf.settings.MEDIA_URL,
    document_root=django.conf.settings.MEDIA_ROOT,
)
