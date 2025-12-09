from rest_framework import permissions


class IsBusinessUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        try:
            return request.user.profile.user_type == 'business'
        except AttributeError:
            return False
