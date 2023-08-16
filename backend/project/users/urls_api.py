from django.urls import path, include

import users.views_api

urlpatterns = [
    path('users/', users.views_api.UserListView.as_view(), name='users-list'),
    path('user_data/<str:username>/', users.views_api.UserInfoView.as_view(), name='users-data'),
]
