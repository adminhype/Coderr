from rest_framework import permissions


class IsCustomerUser(permissions.BasePermission):

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        try:
            return request.user.profile.user_type == 'customer'
        except AttributeError:
            return False
