from django.contrib import admin
from .models import User

# Mendaftarkan Custom User Model agar muncul di Admin Panel
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # Mengatur kolom yang ditampilkan sesuai permintaan Lab nomor 6
    list_display = ('username', 'email', 'is_admin', 'is_member', 'is_staff')
    
    # Opsional: Menambahkan filter di samping agar mudah mencari role
    list_filter = ('is_admin', 'is_member', 'is_staff')