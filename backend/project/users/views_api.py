import django.shortcuts
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

import users.models
from .models import User
from .serializers import UserSerializer, ProfileSerializer


# хорошо сделан
class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    lookup_url_kwarg = 'user_id'
    lookup_field = 'id'
    serializer_class = ProfileSerializer

    def perform_update(self, serializer):
        if serializer.instance == self.request.user:
            serializer.save()
        else:
            raise PermissionDenied('You can only update your own profile.')


class UserSearchListApiView(ListAPIView):
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return users.models.User.objects.filter(username__icontains=self.kwargs['username_filter'])



class UserRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data)
