from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from usermanagement_24782001.api_views import RegisterView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django_scalar.views import scalar_viewer

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('main_app.api_urls')),
    
    # PERBAIKAN: Gunakan format tuple (path, app_name) untuk mendaftarkan namespace
    path('dashboard/', include(('dashboard_24782001.urls', 'dashboard_24782001'), namespace='dashboard_24782001')),
    
    path('', include('main_app.urls')),
    path('about/', include('about.urls')),
    path('contacts/', include('contacts.urls')),
    path('auth/', include('usermanagement_24782001.urls')),
]

urlpatterns += [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', RegisterView.as_view(), name='api_register'),

    # OpenAPI Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/docs/scalar/', scalar_viewer, name='scalar-ui'),
]