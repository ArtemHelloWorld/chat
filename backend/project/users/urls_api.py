from django.urls import path

import users.views_api

urlpatterns = [
    path('user/<int:user_id>/', users.views_api.UserRetrieveUpdateAPIView.as_view(), name='profile-read-update'),
    path('user/register/', users.views_api.UserRegisterView.as_view(), name='user-create'),
]
