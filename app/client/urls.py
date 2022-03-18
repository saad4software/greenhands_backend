from django.urls import path
from .views import *


photos_list = PhotoViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

photos_detail = PhotoViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

user_needs_list = NeedsViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

user_needs_detail = NeedsViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})


urlpatterns = [
    path('anonymous_login/', AnonymousLoginView.as_view()),
    path('register/', RegisterView.as_view()),

    # any user can ask for categories, needs, points and organizers
    path('categories/', CategoriesListView.as_view()),
    path('needs/', NeedsListView.as_view()),
    path('points/', PointsListView.as_view()),
    path('organizers/', OrganizersListView.as_view()),

    # givers only, get list of provided needs and make provide request
    path('giver/provide/', ProvideNeedView.as_view()),

    # organizers only, post to verify, get to list
    path('organizer/requests/', OrganizerRequestsView.as_view()),

    # current user point, needs and photos
    path('user/notifications/', UserNotificationsView.as_view()),
    path('user/photos/', photos_list),
    path('user/photos/<int:id>/', photos_detail),
    path('user/profile/', UserProfileView.as_view()),
    # default password is 12345678
    path('user/password/', UserPasswordView.as_view()),

    # only taker
    path('taker/point/', TakerPointView.as_view()),
    path('taker/needs/', user_needs_list),
    path('taker/needs/<int:id>/', user_needs_detail),

    # taker only, get list of sent verifications requests and make requests
    path('taker/verify/', TakerVerificationView.as_view()),

]

