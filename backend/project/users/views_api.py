import rest_framework.exceptions
import rest_framework.generics
import rest_framework.permissions
import rest_framework.response
import rest_framework.status

import core.validators
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

    def post(self, request, *args, **kwargs):
        password_valid = core.validators.validate_password(request.data.get('password', ''))
        if password_valid is not True:
            return rest_framework.response.Response(
                {'password': password_valid},
                status=rest_framework.status.HTTP_400_BAD_REQUEST
            )

        serializer = users.serializers.UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return rest_framework.response.Response(serializer.data)
