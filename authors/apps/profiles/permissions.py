from rest_framework import permissions


class UserOwnsProfifle(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        """ Determines if a has write access to a given profle"""
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.username == obj.username
