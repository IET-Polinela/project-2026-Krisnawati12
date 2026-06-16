from rest_framework import permissions


class ReportAccessPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated

        if not request.user or not request.user.is_authenticated:
            return False

        if view.action == 'create':
            return not getattr(request.user, 'is_admin', False)

        return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if getattr(request.user, 'is_admin', False):
            if obj.status == 'DRAFT':
                return False

            if view.action == 'destroy':
                return False

            if view.action in ['update', 'partial_update']:
                return set(request.data.keys()) <= {'status'}

            return False

        if view.action in ['update', 'partial_update', 'destroy']:
            return obj.reporter == request.user

        return False


class IsOwnerAndDraftOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.reporter == request.user and obj.status == 'DRAFT'