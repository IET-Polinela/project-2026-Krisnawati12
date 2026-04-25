from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main_app.urls')),
    path('about/', include('about.urls')),
    path('contacts/', include('contacts.urls')),
    
    # Tambahkan baris ini untuk Lab 6 - NPM 24782001
    path('auth/', include('usermanagement_24782001.urls')),
]