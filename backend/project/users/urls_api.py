from django.urls import path, include

import users.views_api

urlpatterns = [
    path('users/all/', users.views_api.UserListView.as_view(), name='users-list'),
    path('user/<str:username>/', users.views_api.UserInfoView.as_view(), name='user-data'),
    path('account/register/', users.views_api.UserRegisterView.as_view(), name='user-create'),
]
