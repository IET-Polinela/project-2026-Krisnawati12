from rest_framework import viewsets, pagination, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Q
from drf_spectacular.utils import extend_schema
from .models import Report
from .serializers import ReportSerializer


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
            if obj.status == 'DRAFT' or view.action == 'destroy':
                return False
            return set(request.data.keys()) <= {'status'}

        return obj.reporter == request.user


class ReportPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class ReportViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, ReportAccessPermission]

    serializer_class = ReportSerializer
    pagination_class = ReportPagination
    queryset = Report.objects.all().order_by('-updated_at')

    def get_queryset(self):
        user = self.request.user
        qs = Report.objects.all().order_by('-updated_at')
        tab = self.request.query_params.get('tab', None)

        if not user or user.is_anonymous:
            return Report.objects.none()

        if getattr(user, 'is_admin', False):
            return qs.exclude(status='DRAFT')

        if tab == 'my_reports':
            return qs.filter(reporter=user)

        if tab == 'feed':
            return qs.exclude(reporter=user).filter(~Q(status='DRAFT'))

        return qs.filter(~Q(status='DRAFT') | Q(reporter=user))

    def perform_create(self, serializer):
        serializer.save(reporter=self.request.user, status='REPORTED')

    def perform_update(self, serializer):
        serializer.save()

    @extend_schema(exclude=True)
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)