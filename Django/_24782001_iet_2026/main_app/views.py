from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Count, Q
from .models import Report

# --- 1. HALAMAN DAFTAR LAPORAN (HOME) ---
class ReportListView(LoginRequiredMixin, ListView):
    model = Report
    template_name = 'main_app/home.html'
    context_object_name = 'reports'
    ordering = ['-pk']
    login_url = 'usermanagement_24782001:login'

    def get_queryset(self):
        # Logika pencarian judul atau lokasi
        query = self.request.GET.get('q')
        if query:
            return Report.objects.filter(
                Q(title__icontains=query) | Q(location__icontains=query)
            ).order_by('-pk')
        return Report.objects.all().order_by('-pk')

# --- 2. DASHBOARD STATISTIK (INDEX.HTML) ---
class DashboardView(LoginRequiredMixin, TemplateView):
    # Jalur ini akan bekerja jika folder dashboard_24782001 sudah di dalam folder templates
    template_name = 'dashboard_24782001/index.html' 
    login_url = 'usermanagement_24782001:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Data grafik (Chart.js) berdasarkan Status dan Kategori
        context['status_data'] = Report.objects.values('status').annotate(total=Count('status'))
        context['category_data'] = Report.objects.values('category').annotate(total=Count('category'))
        
        # Summary angka untuk kartu dashboard
        context['total_reports'] = Report.objects.count()
        context['pending_count'] = Report.objects.filter(status='REPORTED').count()
        context['resolved_count'] = Report.objects.filter(status='RESOLVED').count()
        
        # Laporan terbaru untuk ditampilkan di tabel dashboard
        context['recent_reports'] = Report.objects.filter(status='REPORTED').order_by('-pk')[:5]
        
        return context

# --- 3. DETAIL & CRUD ---
class ReportDetailView(LoginRequiredMixin, DetailView):
    model = Report
    template_name = 'main_app/report_detail.html'
    login_url = 'usermanagement_24782001:login'

class ReportCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Report
    fields = ['title', 'category', 'description', 'location']
    template_name = 'main_app/add_report.html'
    success_url = reverse_lazy('main_app:home')
    success_message = "Laporan berhasil ditambahkan ke Smartvillage Lite! 🚀"
    login_url = 'usermanagement_24782001:login'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_admin:
            messages.error(request, "Akses Ditolak! Hanya Admin yang boleh menambah laporan.")
            return redirect('main_app:home')
        return super().dispatch(request, *args, **kwargs)

class ReportUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Report
    fields = ['title', 'category', 'description', 'location']
    template_name = 'main_app/add_report.html'
    success_url = reverse_lazy('main_app:home')
    success_message = "Data laporan berhasil diupdate! ✅"
    login_url = 'usermanagement_24782001:login'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_admin:
            messages.error(request, "Izin ditolak.")
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
            messages.error(request, "Hanya Admin yang bisa menghapus.")
            return redirect('main_app:home')
        return super().dispatch(request, *args, **kwargs)

# --- 4. WORKFLOW STATUS ---
class ReportUpdateStatusView(LoginRequiredMixin, View):
    login_url = 'usermanagement_24782001:login'

    def post(self, request, pk):
        if not request.user.is_admin:
            return redirect('main_app:home')
            
        report = get_object_or_404(Report, pk=pk)
        
        # Alur status bertahap
        if report.status == 'REPORTED':
            report.status = 'VERIFIED'
        elif report.status == 'VERIFIED':
            report.status = 'IN_PROGRESS'
        elif report.status == 'IN_PROGRESS':
            report.status = 'RESOLVED'
            
        report.save()
        messages.success(request, f"Status '{report.title}' diperbarui.")
        return redirect('main_app:home')