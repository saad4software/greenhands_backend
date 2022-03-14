from rest_framework import permissions


class IsGiver(permissions.BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'role') and (request.user.role == 'G' or request.user.role == 'A')


class IsTaker(permissions.BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'role') and (request.user.role == 'T' or request.user.role == 'A')


class IsOrganizer(permissions.BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'role') and (request.user.role == 'O' or request.user.role == 'A')


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'role') and (request.user.role == 'A')


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method == 'GET' or (hasattr(request.user, 'role') and (request.user.role == 'A'))


class IsTakerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method == 'GET' or (hasattr(request.user, 'role') and (request.user.role == 'T'))

