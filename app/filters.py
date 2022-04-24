from django_filters import rest_framework as filters
from .models import *


class CategoryDataFilter(filters.FilterSet):
    active = filters.BooleanFilter(field_name="active")

    class Meta:
        model = Category
        fields = ['active']


class NeedDataFilter(filters.FilterSet):
    active = filters.BooleanFilter(field_name="active")

    class Meta:
        model = Need
        fields = ['active']


class OrganizersDataFilter(filters.FilterSet):
    min_lat = filters.NumberFilter(field_name='lat', lookup_expr="gte")
    max_lat = filters.NumberFilter(field_name='lat', lookup_expr="lte")
    min_lng = filters.NumberFilter(field_name='lng', lookup_expr="gte")
    max_lng = filters.NumberFilter(field_name='lng', lookup_expr="lte")

    class Meta:
        model = User
        fields = ['min_lat', 'max_lat', 'min_lng', 'max_lng']


class PointsDataFilter(filters.FilterSet):
    min_lat = filters.NumberFilter(field_name='lat', lookup_expr="gte")
    max_lat = filters.NumberFilter(field_name='lat', lookup_expr="lte")
    min_lng = filters.NumberFilter(field_name='lng', lookup_expr="gte")
    max_lng = filters.NumberFilter(field_name='lng', lookup_expr="lte")

    class Meta:
        model = Point
        fields = ['min_lat', 'max_lat', 'min_lng', 'max_lng']


