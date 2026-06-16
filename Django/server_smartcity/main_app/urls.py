from django.urls import path
from . import views

app_name = 'main_app'

urlpatterns = [
    # 1. Halaman Daftar Laporan (Home)
    path('', views.ReportListView.as_view(), name='home'),
    
    # --- BARIS DASHBOARD DI SINI WAJIB DIHAPUS ---
    
    # 3. Fitur Tambah Laporan
    path('add/', views.ReportCreateView.as_view(), name='add_report'),
    
    # 4. Fitur Detail Laporan
    path('detail/<int:pk>/', views.ReportDetailView.as_view(), name='report_detail'),
    
    # 5. Fitur Edit/Update Data Laporan
    path('update/<int:pk>/', views.ReportUpdateView.as_view(), name='update_report'),
    
    # 6. Fitur Hapus Laporan
    path('delete/<int:pk>/', views.ReportDeleteView.as_view(), name='delete_report'),
    
    # 7. Fitur Ganti Status (Workflow)
    path('update-status/<int:pk>/', views.ReportUpdateStatusView.as_view(), name='update_status'),
]