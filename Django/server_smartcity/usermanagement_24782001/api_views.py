from rest_framework import generics, permissions
from .serializers import RegisterSerializer
from django.contrib.auth import get_user_model

class RegisterView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = RegisterSerializer
    # Gunakan AllowAny karena semua orang (termasuk yang belum punya akun) harus bisa mengakses endpoint register ini
    permission_classes = [permissions.AllowAny]