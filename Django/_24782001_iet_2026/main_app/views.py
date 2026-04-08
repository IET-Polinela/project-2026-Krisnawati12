from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from .models import Report

# 1. Menampilkan Daftar Laporan (Ganti 'home')
class ReportListView(ListView):
    model = Report
    template_name = 'main_app/home.html'
    context_object_name = 'reports'

# 2. Menampilkan Detail (Baru di Lab 4)
class ReportDetailView(DetailView):
    model = Report
    template_name = 'main_app/report_detail.html'

# 3. Tambah Laporan (Ganti 'add_report')
class ReportCreateView(CreateView):
    model = Report
    fields = ['title', 'category', 'description', 'location']
    template_name = 'main_app/add_report.html'
    success_url = reverse_lazy('main_app:home')

# 4. Update Laporan (Ganti 'update_report')
class ReportUpdateView(UpdateView):
    model = Report
    fields = ['title', 'category', 'description', 'location']
    template_name = 'main_app/add_report.html' # Bisa pakai template yang sama dengan Create
    success_url = reverse_lazy('main_app:home')

# 5. Hapus Laporan (Ganti 'delete_report')
class ReportDeleteView(DeleteView):
    model = Report
    template_name = 'main_app/report_confirm_delete.html'
    success_url = reverse_lazy('main_app:home')

# 6. Workflow Khusus Perubahan Status
class ReportUpdateStatusView(View):
    def post(self, request, pk):
        report = get_object_or_404(Report, pk=pk)
        new_status = request.POST.get('status')
        report.status = new_status
        report.save()
        return redirect('main_app:home')