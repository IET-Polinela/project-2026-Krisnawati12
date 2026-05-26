from rest_framework import serializers
from django.contrib.auth import get_user_model

# Mengambil model CustomUser yang aktif (usermanagement_24782001.User)
User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    # Kolom password diset write_only agar tidak ikut menampilkan password saat data di-return
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        # WAJIB menggunakan create_user agar password warga otomatis di-hash (didekripsi aman) oleh Django
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user