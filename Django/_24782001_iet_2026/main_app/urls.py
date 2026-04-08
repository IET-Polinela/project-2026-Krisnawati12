from django.urls import path
from . import views

app_name = 'main_app'

urlpatterns = [
    # Tampilan Utama (Daftar Laporan)
    path('', views.ReportListView.as_view(), name='home'),
    
    # Tambah Laporan
    path('add/', views.ReportCreateView.as_view(), name='add_report'),
    
    # Detail Laporan (Baru di Lab 4)
    path('detail/<int:pk>/', views.ReportDetailView.as_view(), name='report_detail'),
    
    # Update/Edit Data Laporan
    path('update/<int:pk>/', views.ReportUpdateView.as_view(), name='update_report'),
    
    # Hapus Laporan
    path('delete/<int:pk>/', views.ReportDeleteView.as_view(), name='delete_report'),
    
    # KHUSUS WORKFLOW: Update Status (Sesuai instruksi nomor 3)
    path('update-status/<int:pk>/', views.ReportUpdateStatusView.as_view(), name='update_status'),
]