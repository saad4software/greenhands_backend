import os
from django.conf import settings
from rest_framework.exceptions import APIException
from rest_framework import generics, status
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.parsers import FormParser, MultiPartParser
import rest_framework.filters
from rest_framework.permissions import IsAuthenticated
import rest_framework.filters
from app.utils import *
from app.filters import *
from .serializers import *
from app.permissions import *
from app.msgs import *


# manage create, edit, update and delete operations for Need model
class PointViewSet(ModelViewSet):
    permission_classes = (IsAdmin, )
    lookup_field = 'id'

    queryset = Need.objects.all()
    serializer_class = NeedSerializer
    pagination_class = StandardResultsSetPagination
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]
    filter_backends = [filters.DjangoFilterBackend, rest_framework.filters.SearchFilter]
    filterset_class = NeedDataFilter
    search_fields = ['name', 'category.name', 'brief', ]


class PhotoSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.SlugRelatedField(read_only=True, slug_field='id')
    username = serializers.CharField(source='owner.username', read_only=True)
    name = serializers.CharField(source='datafile', read_only=True)

    class Meta:
        model = Photo
        fields = ['created', 'datafile', 'owner', 'username', 'width', 'height', 'active', 'name', 'id']
        read_only_fields = ('created', 'datafile', 'username', 'id', 'width', 'height')


# manage create, edit, update and delete operations for Category model
class CategoryViewSet(ModelViewSet):
    permission_classes = (IsAdminOrReadOnly, )
    lookup_field = 'id'

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = StandardResultsSetPagination
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]
    filter_backends = [filters.DjangoFilterBackend, rest_framework.filters.SearchFilter]
    filterset_class = CategoryDataFilter
    search_fields = ['name', ]


# manage create, edit, update and delete operations for Need model
class NeedViewSet(ModelViewSet):
    permission_classes = (IsAdmin, )
    lookup_field = 'id'

    queryset = Need.objects.all()
    serializer_class = NeedSerializer
    pagination_class = StandardResultsSetPagination
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]
    filter_backends = [filters.DjangoFilterBackend, rest_framework.filters.SearchFilter]
    filterset_class = NeedDataFilter
    search_fields = ['name', 'category.name', 'brief', ]
