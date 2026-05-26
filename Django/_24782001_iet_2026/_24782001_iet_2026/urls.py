from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
# Impor RegisterView dari app usermanagement
from usermanagement_24782001.api_views import RegisterView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Lab 9 - API Endpoint 
    path('api/', include('main_app.api_urls')), 
    
    # Dashboard & Web Template lama
    path('dashboard/', include('dashboard_24782001.urls')),
    path('', include('main_app.urls')),
    path('about/', include('about.urls')),
    path('contacts/', include('contacts.urls')),
    path('auth/', include('usermanagement_24782001.urls')),
]

# Lab 10 - Routing Token & Register API
urlpatterns += [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', RegisterView.as_view(), name='api_register'), # Endpoint Register Warga Baru
]