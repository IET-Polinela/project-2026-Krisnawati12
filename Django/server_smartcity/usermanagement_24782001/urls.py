from django.urls import path
from . import views

app_name = 'usermanagement_24782001'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
]