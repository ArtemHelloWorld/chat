import django.contrib.auth.password_validation
import django.core.exceptions
import rest_framework.serializers
import rest_framework.response
import rest_framework.status

import users.models


class UserSerializer(rest_framework.serializers.ModelSerializer):
    class Meta:
        model = users.models.User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
        ]

    def validate_password(self, password):
        try:
            django.contrib.auth.password_validation.validate_password(
                password=password
            )
        except django.core.exceptions.ValidationError as e:
            raise rest_framework.serializers.ValidationError(e.messages)
        return password

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
