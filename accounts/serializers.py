from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'created_at']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password']

    def validate(self, attrs):
        email = attrs.get('email', None)
        password = attrs.get('password', None)

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            if not user.check_password(password):
                raise serializers.ValidationError('Check Your Email or Password')
        else:
            raise serializers.ValidationError("User does not exist")

        token = RefreshToken.for_user(user=user)
        data = {
            'refresh_token': str(token),
            'access_token': str(token.access_token)
        }
        return data
