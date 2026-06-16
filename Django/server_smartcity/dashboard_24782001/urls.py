from django.urls import path
from . import views

app_name = 'dashboard_24782001'

urlpatterns = [
    # 1. Halaman Utama Dashboard (TemplateView)
    path('', views.DashboardView.as_view(), name='index'),
    
    # 2. API untuk Data Statistik (Chart.js)
    path('api/stats/', views.report_stats_api, name='report_stats_api'),

    # 3. API untuk Fitur Live Search
    path('api/search/', views.report_search_api, name='report_search_api'),

    # 4. API untuk Detail Laporan (Modal/AJAX)
    path('api/detail/<int:report_id>/', views.report_detail_api, name='report_detail_api'),
]