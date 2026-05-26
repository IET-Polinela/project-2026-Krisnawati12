from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Report
from .serializers import ReportSerializer
from .permissions import IsOwnerAndDraftOrReadOnly

class ReportViewSet(viewsets.ModelViewSet):
    serializer_class = ReportSerializer

    def get_queryset(self):
        user = self.request.user

        if hasattr(user, 'is_admin') and user.is_admin:
            return Report.objects.exclude(status='DRAFT')
        
        from django.db.models import Q
        return Report.objects.filter(
            Q(reporter=user) | ~Q(status='DRAFT')
        )

    def get_permissions(self):
        if self.action == 'destroy':
            class IsCitizenOnlyForDelete(permissions.BasePermission):
                def has_permission(self, request, view):
                    if hasattr(request.user, 'is_admin') and request.user.is_admin:
                        return False
                    return True
            return [permissions.IsAuthenticated(), IsCitizenOnlyForDelete(), IsOwnerAndDraftOrReadOnly()]

        if self.action in ['update', 'partial_update']:
            class AllowAdminOrOwner(permissions.BasePermission):
                def has_object_permission(self, request, view, obj):
                    if hasattr(request.user, 'is_admin') and request.user.is_admin:
                        return True
                    return obj.reporter == request.user and obj.status == 'DRAFT'
            return [permissions.IsAuthenticated(), AllowAdminOrOwner()]
        
        if self.action == 'create':
            class IsCitizenOnly(permissions.BasePermission):
                def has_permission(self, request, view):
                    if hasattr(request.user, 'is_admin') and request.user.is_admin:
                        return False
                    return True
            return [permissions.IsAuthenticated(), IsCitizenOnly()]

        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(reporter=self.request.user)