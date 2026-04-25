from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from .models import Report

# --- DASHBOARD (Dapat diakses Citizen & Admin) ---
class ReportListView(LoginRequiredMixin, ListView):
    model = Report
    template_name = 'main_app/home.html'
    context_object_name = 'reports'
    ordering = ['-pk']
    login_url = 'usermanagement_24782001:login'

class ReportDetailView(LoginRequiredMixin, DetailView):
    model = Report
    template_name = 'main_app/report_detail.html'
    login_url = 'usermanagement_24782001:login'

# --- CRUD OPERATIONS (Proteksi Ketat: Khusus Admin) ---

class ReportCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Report
    fields = ['title', 'category', 'description', 'location']
    template_name = 'main_app/add_report.html'
    success_url = reverse_lazy('main_app:home')
    success_message = "Laporan baru berhasil dikirim oleh Admin! 🚀"
    login_url = 'usermanagement_24782001:login'

    def dispatch(self, request, *args, **kwargs):
        # Proteksi Level View: Jika bukan admin, tendang ke home dengan pesan error [cite: 43, 57]
        if not request.user.is_admin:
            messages.error(request, "Akses Ditolak! Hanya Admin yang boleh menambah laporan.")
            return redirect('main_app:home')
        return super().dispatch(request, *args, **kwargs)

class ReportUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Report
    fields = ['title', 'category', 'description', 'location']
    template_name = 'main_app/add_report.html'
    success_url = reverse_lazy('main_app:home')
    success_message = "Data laporan berhasil diperbarui! ✅"
    login_url = 'usermanagement_24782001:login'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_admin:
            messages.error(request, "Akses Ditolak! Anda tidak memiliki izin mengedit laporan.")
            return redirect('main_app:home')
        return super().dispatch(request, *args, **kwargs)

class ReportDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Report
    template_name = 'main_app/report_confirm_delete.html'
    success_url = reverse_lazy('main_app:home')
    success_message = "Laporan telah dihapus dari sistem."
    login_url = 'usermanagement_24782001:login'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_admin:
            messages.error(request, "Akses Ditolak! Hanya Admin yang boleh menghapus laporan.")
            return redirect('main_app:home')
        return super().dispatch(request, *args, **kwargs)

# --- STATUS WORKFLOW (Khusus Admin) ---
class ReportUpdateStatusView(LoginRequiredMixin, View):
    login_url = 'usermanagement_24782001:login'

    def post(self, request, pk):
        # 1. Validasi Peran Admin
        if not request.user.is_admin:
            messages.error(request, "Akses Ditolak! Anda tidak memiliki izin mengubah status.")
            return redirect('main_app:home')
            
        # 2. Ambil Data Report dengan aman
        report = get_object_or_404(Report, pk=pk)
        
        # 3. Logika Workflow Berjenjang (Menghindari NameError)
        if report.status == 'REPORTED':
            report.status = 'VERIFIED'
            messages.info(request, f"Laporan '{report.title}' berhasil diverifikasi.")
        elif report.status == 'VERIFIED':
            report.status = 'RESOLVED'
            messages.success(request, f"Laporan '{report.title}' telah selesai ditangani!")
        else:
            messages.warning(request, "Laporan sudah berada di status final.")
            
        report.save()
        return redirect('main_app:home')