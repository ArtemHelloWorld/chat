import rest_framework.exceptions
import rest_framework.generics
import rest_framework.permissions
import rest_framework.response
import rest_framework.status

import users.models
import users.serializers


# хорошо сделан
class UserRetrieveUpdateAPIView(rest_framework.generics.RetrieveUpdateAPIView):
    queryset = users.models.User.objects.all()
    lookup_url_kwarg = 'user_id'
    lookup_field = 'id'
    serializer_class = users.serializers.ProfileSerializer

    def perform_update(self, serializer):
        if serializer.instance == self.request.user:
            serializer.save()
        else:
            raise rest_framework.exceptions.PermissionDenied(
                'You can only update your own profile.'
            )


class UserSearchListApiView(rest_framework.generics.ListAPIView):
    serializer_class = users.serializers.ProfileSerializer

    def get_queryset(self):
        return users.models.User.objects.filter(
            username__icontains=self.kwargs['username_filter']
        )


class UserRegisterView(rest_framework.generics.CreateAPIView):
    permission_classes = [rest_framework.permissions.AllowAny]
    serializer_class = users.serializers.UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return rest_framework.response.Response(serializer.data)
