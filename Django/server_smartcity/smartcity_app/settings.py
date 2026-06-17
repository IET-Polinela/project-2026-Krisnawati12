"""
Django settings for _24782001_iet_2026 project.
"""

from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-_hm3pf7ods&p)74=t7n-hbyi&0&f=45e(1(*z4jetv6@_=ar+k'
DEBUG = True
ALLOWED_HOSTS = ['*']  # Mengizinkan server diakses dari host/IP mana pun selama praktikum

# --- APPLICATION DEFINITION ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Lab 11 Tambahan Baru: Library Pengatur CORS (Mengizinkan komunikasi lintas port)
    'corsheaders',  # Pastikan ini ada
    
    # Lab 9 & 10 Tambahan REST Framework
    'rest_framework',
    'drf_spectacular',       # ← TAMBAH INI
    'django_scalar',         # ← TAMBAH INI
    
    # Aplikasi Utama & Tugas Kelompokmu
    'main_app',
    'about',
    'contacts',
    'usermanagement_24782001',
    'dashboard_24782001', 
]

# Konfigurasi User Custom Lab 6
AUTH_USER_MODEL = 'usermanagement_24782001.User'

MIDDLEWARE = [
    # Lab 11 Tambahan Baru: WAJIB diletakkan di urutan paling atas sebelum CommonMiddleware!
    'corsheaders.middleware.CorsMiddleware',  # Harus di paling atas / sebelum CommonMiddleware
    
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# pastikan ROOT_URLCONF mengarah ke package yang benar
ROOT_URLCONF = 'smartcity_app.urls'

# pastikan WSGI_APPLICATION mengarah ke modul wsgi yang benar
WSGI_APPLICATION = 'smartcity_app.wsgi.application'

# --- TEMPLATES CONFIGURATION ---
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], 
        'APP_DIRS': True, # Ini yang akan membaca folder templates di dalam app dashboard
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# --- DATABASE CONFIGURATION ---
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'smartcity_db',
        'USER': 'postgres',
        'PASSWORD': 'krisnaijo',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

# Internationalization
LANGUAGE_CODE = 'id'
TIME_ZONE = 'Asia/Jakarta'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static'] 

# Menentukan folder tempat mengumpulkan file statis (untuk tampilan Django Admin/DRF)
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Redirects
LOGIN_REDIRECT_URL = 'main_app:home'
LOGOUT_REDIRECT_URL = 'main_app:home'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- REST FRAMEWORK CONFIGURATION FOR JWT ---
# Konfigurasi otentikasi stateless menggunakan SimpleJWT sesuai modul
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# ----------------------------------------------------------------------
# Lab 11 Tambahan Baru: Konfigurasi Izin Port Frontend Local Web Server
# ----------------------------------------------------------------------
CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:5500",
    "http://localhost:5500",
]
CORS_ALLOW_CREDENTIALS = True
CSRF_TRUSTED_ORIGINS = ["http://127.0.0.1:5500"]

SPECTACULAR_SETTINGS = {
    'TITLE': 'Smart City Portal API',
    'DESCRIPTION': 'Dokumentasi REST API resmi untuk Portal Pelaporan Laporan Warga',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}