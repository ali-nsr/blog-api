from rest_framework import permissions


class IsArticleAuthor(permissions.BasePermission):
    """
    override BasePermission class to create custom permissions
    this one checks if current user is the author or not
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user
