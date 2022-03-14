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

my_needs_list = NeedsViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

my_needs_detail = NeedsViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})


urlpatterns = [
    path('anonymous_login/', AnonymousLoginView.as_view()),
    path('login/', LoginView.as_view()),
    path('register/', RegisterView.as_view()),

    # any user can ask for categories, needs and points
    path('categories/', CategoriesListView.as_view()),
    path('needs/', NeedsListView.as_view()),
    path('points/', PointsListView.as_view()),

    # only giver
    path('provide_need/', ProvideNeedView.as_view()),

    # only for organizer, post to verify, get to list
    path('verify_requests/', VerifyRequestsListView.as_view()),

    # current user point, needs and photos
    path('my_notifications/', NotificationListView.as_view()),
    path('my_photos/', photos_list),
    path('my_photos/<int:id>/', photos_detail),
    path('my_profile/', ProfileView.as_view()),
    # default password is 12345678
    path('my_password/', ChangePasswordView.as_view()),

    # only taker
    path('my_point/', PointView.as_view()),
    path('my_needs/', my_needs_list),
    path('my_needs/<int:id>/', my_needs_detail),
    path('verify_account/', UserVerificationRequestsView.as_view()),

]

