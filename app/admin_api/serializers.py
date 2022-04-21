from rest_framework import serializers
from app.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'role',
            'address',
            'phone',
            'verified_by',
            'lat',
            'lng',
            'is_active',
        ]
        ordering = ['username']


class VerificationCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerificationRequest
        fields = [
            'sender',
            'organizer',
            'code',
            'status',
            'created',
            'active',
        ]
        ordering = ['sender.username']


class NeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Need
        fields = [
            'name',
            'id',
            'images',
            'brief',
            'category',
        ]
        ordering = ['name']


class PhotoSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.SlugRelatedField(read_only=True, slug_field='id')
    username = serializers.CharField(source='owner.username', read_only=True)
    name = serializers.CharField(source='datafile', read_only=True)

    class Meta:
        model = Photo
        fields = [
            'created',
            'datafile',
            'owner',
            'username',
            'width',
            'height',
            'active',
            'name',
            'id',
        ]
        read_only_fields = ('created', 'datafile', 'username', 'id', 'width', 'height')


class CategorySerializer(serializers.ModelSerializer):
    image_model = PhotoSerializer(source='image', read_only=True)

    class Meta:
        model = Category
        fields = [
            'name',
            'id',
            'active',
            'image',
            'image_model',
        ]
        ordering = ['name']


class PointSerializer(serializers.ModelSerializer):

    class Meta:
        model = Point
        fields = [
            'created',
            'name',
            'images',
            'lat',
            'lng',
            'brief',
            'address',
            'user',
            'active',

        ]
        ordering = ['name']


class ReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = Report
        fields = [
            'created',
            'user',
            'sender',
            'title',
            'brief',
            'active',

        ]
        ordering = ['title']


class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Report
        fields = [
            'created',
            'user',
            'sender',
            'title',
            'brief',
            'active',

        ]
        ordering = ['title']


