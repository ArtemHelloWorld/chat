import django.shortcuts
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import UserSerializer


class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class UserInfoView(APIView):
    # возвращаем информацию о пользователе
    permission_classes = [IsAuthenticated]

    def get(self, request, username):
        user = django.shortcuts.get_object_or_404(User, username=username)
        response_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
        }
        return Response(response_data)


class UserRegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data)
