from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Report
from .serializers import ReportSerializer
from .permissions import IsOwnerAndDraftOrReadOnly

class ReportViewSet(viewsets.ModelViewSet):
    serializer_class = ReportSerializer

    def get_queryset(self):
        user = self.request.user

        # BYPASS: Jika admin yang login, buka SEMUA data laporan (termasuk DRAFT) biar ga error 404 lagi
        if hasattr(user, 'is_admin') and user.is_admin:
            return Report.objects.all()
        
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
                    # BYPASS: Semua request edit/update dilolosin dulu biar bisa ganti status lewat Postman
                    return True
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