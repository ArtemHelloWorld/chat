from django.urls import path, include

import users.views_api

urlpatterns = [
    path('users/all/', users.views_api.UserListView.as_view(), name='users-list'),
    path('profile/<str:user_id>/', users.views_api.ProfileRetrieveUpdateAPIView.as_view(), name='profile-read-update'),
    path('account/register/', users.views_api.UserRegisterView.as_view(), name='user-create'),
]
