from rest_framework.permissions import BasePermission

class IsAdminOrAuthenticated(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return request.user and (request.user.is_staff or request.user.is_authenticated)
        elif request.method == 'POST':
            return request.user and request.user.is_staff
        elif request.method == 'PATCH':
            return request.user and (request.user.is_authenticated or request.user.is_staff)
        elif request.method == 'DELETE':
            return request.user and request.user.is_staff
        return False