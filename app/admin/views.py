from rest_framework.viewsets import ModelViewSet
import rest_framework.filters
import rest_framework.filters
from app.utils import *
from app.filters import *
from .serializers import *
from app.permissions import *


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
    search_fields = [
        'name',
        'category.name',
        'brief',
    ]


class UserViewSet(ModelViewSet):
    permission_classes = (IsAdmin, )
    lookup_field = 'id'

    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = StandardResultsSetPagination
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]
    filter_backends = [filters.DjangoFilterBackend, rest_framework.filters.SearchFilter]
    filterset_class = NeedDataFilter
    search_fields = [
        'username',
        'first_name',
        'last_name',
    ]


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


class PhotoViewSet(ModelViewSet):
    permission_classes = (IsAdmin, )
    lookup_field = 'id'

    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    pagination_class = StandardResultsSetPagination
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]
    filter_backends = [filters.DjangoFilterBackend, rest_framework.filters.SearchFilter]
    filterset_class = NeedDataFilter
    search_fields = ['datafile', 'brief', ]


class NotificationsViewSet(ModelViewSet):
    permission_classes = (IsAdmin, )
    lookup_field = 'id'

    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    pagination_class = StandardResultsSetPagination
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]
    filter_backends = [filters.DjangoFilterBackend, rest_framework.filters.SearchFilter]
    filterset_class = NeedDataFilter
    search_fields = ['title', 'brief', ]


class RequestsViewSet(ModelViewSet):
    permission_classes = (IsAdmin, )
    lookup_field = 'id'

    queryset = VerificationRequest.objects.all()
    serializer_class = VerificationCodeSerializer
    pagination_class = StandardResultsSetPagination
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]
    filter_backends = [filters.DjangoFilterBackend, rest_framework.filters.SearchFilter]
    filterset_class = NeedDataFilter
    search_fields = ['title', 'brief', ]


