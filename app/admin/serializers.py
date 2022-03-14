from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from app.models import *
from app.msgs import *


class NeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Need
        fields = ['name', 'id', 'images', 'brief', 'category']
        ordering = ['name']


class PhotoSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.SlugRelatedField(read_only=True, slug_field='id')
    username = serializers.CharField(source='owner.username', read_only=True)
    name = serializers.CharField(source='datafile', read_only=True)

    class Meta:
        model = Photo
        fields = ['created', 'datafile', 'owner', 'username', 'width', 'height', 'active', 'name', 'id']
        read_only_fields = ('created', 'datafile', 'username', 'id', 'width', 'height')


class CategorySerializer(serializers.ModelSerializer):
    image_model = PhotoSerializer(source='image', read_only=True)

    class Meta:
        model = Category
        fields = ['name', 'id', 'active', 'image', 'image_model']
        ordering = ['name']

