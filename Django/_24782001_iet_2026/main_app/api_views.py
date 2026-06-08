from rest_framework import viewsets, pagination, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Q
from .models import Report
from .serializers import ReportSerializer


class ReportPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class ReportViewSet(viewsets.ModelViewSet):
    # JWT Authentication
    authentication_classes = [JWTAuthentication]

    # User login boleh POST, guest hanya baca
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    serializer_class = ReportSerializer
    pagination_class = ReportPagination
    queryset = Report.objects.all().order_by('-updated_at')

    def get_queryset(self):
        user = self.request.user
        qs = Report.objects.all().order_by('-updated_at')
        tab = self.request.query_params.get('tab', None)

        # PERBAIKAN: hindari error AnonymousUser
        if not user or user.is_anonymous:
            return Report.objects.none()

        if tab == 'my_reports':
            return qs.filter(reporter=user)

        if tab == 'feed':
            return qs.exclude(reporter=user).filter(~Q(status='DRAFT'))

        return qs.filter(~Q(status='DRAFT') | Q(reporter=user))

    def perform_create(self, serializer):
        serializer.save(reporter=self.request.user)

    def perform_update(self, serializer):
        serializer.save()