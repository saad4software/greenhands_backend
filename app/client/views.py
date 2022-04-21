import os
from django.conf import settings
from django.db.models import *
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


# anonymous login for givers and takers
class AnonymousLoginView(TokenViewBase):
    serializer_class = AnonymousLoginSerializer
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]


# register organizers
class RegisterView(generics.CreateAPIView):
    permission_classes = ()

    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]

    def perform_create(self, serializer):
        # activating organizers account requires admin manual approval
        serializer.save(is_active=False)


# manage create, edit, update and delete operations for Photo model
class PhotoViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'
    pagination_class = StandardResultsSetPagination
    serializer_class = PhotoSerializer
    parser_classes = (MultiPartParser, FormParser,)
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]
    filter_backends = [rest_framework.filters.SearchFilter]
    search_fields = ['datafile']

    def get_queryset(self):
        return Photo.objects.filter(active=True, owner=self.request.user)

    # remove the photo file when removing photo instance
    def perform_destroy(self, instance):
        instance.delete()
        os.remove(os.path.join(settings.MEDIA_ROOT, instance.datafile.name))

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user, datafile=self.request.data.get('datafile'))


# manage taker point, one point, multiple needs
class TakerPointView(APIView):
    permission_classes = (IsTaker,)
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]

    def get(self, request):
        point = Point.objects.filter(user=request.user).first()
        if not point:
            raise APIException(error_no_point)

        serializer = PointSerializer(point)
        return Response(serializer.data)

    def post(self, request):
        point = Point.objects.filter(user=request.user).first()
        serializer = PointSerializer(point, data=request.data) if point else PointSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
        raise APIException(serializer.errors)

    def delete(self, request):
        point = Point.objects.filter(user=request.user).first()
        if not Point:
            raise APIException(error_no_point)

        point.active = False
        point.save()
        return Response(msg_success)


# manage taker needs, should have a point
class NeedsViewSet(ModelViewSet):
    permission_classes = (IsTaker,)
    lookup_field = 'id'

    serializer_class = NeedSerializer
    pagination_class = StandardResultsSetPagination
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]
    filter_backends = [filters.DjangoFilterBackend, rest_framework.filters.SearchFilter]
    filterset_class = NeedDataFilter
    search_fields = ['name', 'place__name', 'category__name']

    def perform_create(self, serializer):
        point = Point.objects.filter(active=True, user=self.request.user).first()
        if not point:
            raise APIException(error_no_point)

        serializer.save(point=point)

    def perform_update(self, serializer):
        # todo: can taker edit active needs?
        # need = self.get_queryset().filter(pk=self.request.data['id']).first()
        # if need.editable:
        #     serializer.save()
        serializer.save()

    def get_queryset(self):
        point = Point.objects.filter(active=True, user=self.request.user).first()
        return Need.objects.filter(point=point)

    # remove the photo file when removing photo instance
    def perform_destroy(self, instance):
        instance.active = False
        instance.save()


# list needs categories
class CategoriesListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'
    pagination_class = StandardResultsSetPagination
    serializer_class = CategorySerializer
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]
    filter_backends = [rest_framework.filters.SearchFilter]
    search_fields = ['name']

    def get_queryset(self):
        return Category.objects.filter(active=True)


# query active organizers
class OrganizersListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, )
    lookup_field = 'id'
    serializer_class = UserSerializer
    pagination_class = StandardResultsSetPagination
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]
    filter_backends = [filters.DjangoFilterBackend, rest_framework.filters.SearchFilter]
    search_fields = ['address', 'phone', 'first_name', 'last_name']

    def get_queryset(self):
        queryset = User.objects.filter(
            is_active=True,
            role="O",
        )
        return queryset


# query active points, needs should be attached to points
class PointsListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, ]
    lookup_field = 'id'
    serializer_class = PointSerializer
    pagination_class = StandardResultsSetPagination
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]
    filter_backends = [filters.DjangoFilterBackend, rest_framework.filters.SearchFilter]
    search_fields = ['name', 'brief', 'address']

    def get_queryset(self):
        queryset = Point.objects.annotate(
            needs_count=Count('needs', filter=Q(needs__active=True, needs__giver=None))
        ).filter(
            active=True,
            needs_count__gt=0
        )
        return queryset


# query active points, needs should be attached to points
class UserNotificationsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, ]
    lookup_field = 'id'
    serializer_class = NotificationSerializer
    pagination_class = StandardResultsSetPagination
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]
    filter_backends = [filters.DjangoFilterBackend, rest_framework.filters.SearchFilter]
    search_fields = ['title', 'brief']

    def get_queryset(self):
        queryset = Notification.objects.filter(
            active=True,
            user=self.request.user
        )
        return queryset


# query active needs
class NeedsListView(generics.ListAPIView):
    permission_classes = ()
    lookup_field = 'id'
    serializer_class = NeedSerializer
    pagination_class = StandardResultsSetPagination
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]
    filter_backends = [filters.DjangoFilterBackend, rest_framework.filters.SearchFilter]
    search_fields = ['name', 'brief', 'category__name', 'point__name']

    def get_queryset(self):
        queryset = Need.objects.filter(
            active=True,
            giver=None
        )
        return queryset


# query request sent to organizers
class OrganizerRequestsView(generics.ListAPIView):
    permission_classes = (IsOrganizer, )
    lookup_field = 'id'
    serializer_class = VerificationRequestSerializer
    pagination_class = StandardResultsSetPagination
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]
    filter_backends = [filters.DjangoFilterBackend, rest_framework.filters.SearchFilter]

    def get_queryset(self):
        queryset = VerificationRequest.objects.filter(
            active=True,
            organizer=self.request.user
        )
        return queryset

    def post(self, request, *args, **kwargs):
        serializer = ConfirmRequestSerializer(data=request.data, context=request)
        if serializer.is_valid():
            serializer.save()
            return Response(msg_success)
        raise APIException(serializer.errors)


class UserProfileView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]

    def get(self, request):
        serializer = UserUpdateSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = UserUpdateSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        print(serializer.errors)
        raise APIException(serializer.errors)


class UserPasswordView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]

    def post(self, request, *args, **kwargs):
        serializer = UserChangePasswordSerializer(data=request.data, context=request)

        if serializer.is_valid():
            return Response(msg_success)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProvideNeedView(APIView):
    permission_classes = (IsGiver,)
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]

    def get(self, request):
        qs = Need.objects.filter(giver=request.user)
        serializer = NeedSerializer(qs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProvideNeedSerializer(data=request.data)
        if serializer.is_valid():
            need = serializer.get_instance(request.data['need_id'])
            need.giver = request.user
            need.save()
            notification = Notification(
                user=need.point.user,
                sender=request.user,
                title=need.name,
                brief=serializer.data.get('message')
            )
            notification.save()
            return Response(msg_success)
        raise APIException(serializer.errors)


class TakerVerificationView(APIView):
    permission_classes = (IsTaker or IsGiver,)
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]

    def get(self, request):
        qs = VerificationRequest.objects.filter(sender=request.user)
        serializer = VerificationRequestSerializer(qs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = VerificationRequestSerializer(data=request.data)
        if serializer.is_valid():
            organizer = serializer.get_organizer(request.data['organizer_id'])
            sent = VerificationRequest.objects.filter(sender=request.user, organizer=organizer).exists()
            if sent:
                raise APIException('already_sent')

            user_serializer = UserDataCheckSerializer(data=request.user.__dict__)
            if not user_serializer.is_valid():
                raise APIException(user_serializer.errors)

            verification_request = VerificationRequest(
                sender=request.user,
                organizer=organizer,
            )
            verification_request.save()
            print(serializer.data.get('message'))
            notification = Notification(
                user=organizer,
                sender=request.user,
                title=request.user.first_name,
                brief=serializer.data.get('message')
            )
            notification.save()
            return Response(msg_success)
        raise APIException(serializer.errors)



