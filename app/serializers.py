from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from app.models import *
from .msgs import *
from django.core.mail import send_mail


class LoginSerializer(TokenObtainPairSerializer):

    # cannot user default token validator since i'm using email (not username) for login
    def validate(self, attrs):
        # data = super().validate(attrs)
        user = get_user_model().objects.filter(email=attrs['username']).first()
        if not user or not user.check_password(attrs['password']):
            raise serializers.ValidationError(error_invalid_credentials)
        refresh = self.get_token(user)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'role': str(user.role)
        }
        return data

