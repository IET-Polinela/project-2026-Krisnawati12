from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Dashboard ditaruh di ATAS path kosong ('')
    path('dashboard/', include('dashboard_24782001.urls')),
    
    # Home/Main app ditaruh di bawah
    path('', include('main_app.urls')),
    
    path('about/', include('about.urls')),
    path('contacts/', include('contacts.urls')),
    path('auth/', include('usermanagement_24782001.urls')),
]