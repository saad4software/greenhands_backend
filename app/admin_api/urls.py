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

points_list = PointViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

point_detail = PointViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

users_list = UserViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

user_detail = UserViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

categories_list = CategoryViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

category_detail = CategoryViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

needs_list = NeedViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

need_detail = NeedViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

requests_list = RequestsViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

request_detail = RequestsViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

notifications_list = NotificationsViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

notification_detail = NotificationsViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    path('photos/', photos_list),
    path('photos/<int:id>/', photos_detail),

    path('categories/', categories_list),
    path('categories/<int:id>/', category_detail),

    path('users/', users_list),
    path('users/<int:id>/', user_detail),

    path('points/', points_list),
    path('points/<int:id>/', point_detail),

    path('needs/', needs_list),
    path('needs/<int:id>/', need_detail),

    path('requests/', requests_list),
    path('requests/<int:id>/', request_detail),

    path('notifications/', notifications_list),
    path('notifications/<int:id>/', notification_detail),

]



