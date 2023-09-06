import rest_framework

import users.models


class UserSerializer(rest_framework.serializers.ModelSerializer):
    class Meta:
        model = users.models.User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'password',
        ]

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = users.models.User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class ProfileSerializer(rest_framework.serializers.ModelSerializer):
    class Meta:
        model = users.models.User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'bio',
            'profile_image',
        ]
        # fields += ['email', 'is_online', 'last_online']
