from rest_framework import permissions


class IsManager(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_permission(self, request, view):
        if request.user.profile.group == "admin":
            return True
        return False
