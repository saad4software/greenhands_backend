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


