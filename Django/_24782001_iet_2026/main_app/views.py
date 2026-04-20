from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin # Mixin khusus untuk CBV
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from .models import Report

# 1. Menampilkan Daftar Laporan
class ReportListView(ListView):
    model = Report
    template_name = 'main_app/home.html'
    context_object_name = 'reports'
    ordering = ['-pk'] # Tambahan: laporan terbaru muncul paling atas

# 2. Menampilkan Detail
class ReportDetailView(DetailView):
    model = Report
    template_name = 'main_app/report_detail.html'

# 3. Tambah Laporan (Gunakan SuccessMessageMixin)
# Copy bagian ini aja kalau mau ganti ReportCreateView kamu:
class ReportCreateView(SuccessMessageMixin, CreateView):
    model = Report
    fields = ['title', 'category', 'description', 'location']
    template_name = 'main_app/add_report.html'
    success_url = reverse_lazy('main_app:home')
    
    # POIN 8: Pesan yang muncul di kotak Alert (Warna Hijau)
    success_message = "Laporan baru berhasil dikirim! 🚀"

    # POIN 7: Trik buat ngetes Loading Feedback (Biar tombol muter agak lama)
    def form_valid(self, form):
        import time
        time.sleep(2) # Menunda simpan 2 detik biar efek "Loading..." kelihatan
        return super().form_valid(form)

# 4. Update Laporan
class ReportUpdateView(SuccessMessageMixin, UpdateView):
    model = Report
    fields = ['title', 'category', 'description', 'location']
    template_name = 'main_app/add_report.html'
    success_url = reverse_lazy('main_app:home')
    success_message = "Data laporan berhasil diperbarui! ✅" # Poin 8

# 5. Hapus Laporan
class ReportDeleteView(DeleteView):
    model = Report
    template_name = 'main_app/report_confirm_delete.html'
    success_url = reverse_lazy('main_app:home')

    # DeleteView tidak mendukung SuccessMessageMixin secara langsung, jadi pakai ini:
    def delete(self, request, *args, **kwargs):
        messages.error(self.request, "Laporan telah dihapus dari sistem.") # Poin 8
        return super().delete(request, *args, **kwargs)

# 6. Workflow Khusus Perubahan Status
class ReportUpdateStatusView(View):
    def post(self, request, pk):
        report = get_object_or_404(Report, pk=pk)
        new_status = request.POST.get('status')
        report.status = new_status
        report.save()
        
        # Berikan feedback sesuai status baru
        messages.info(request, f"Status laporan '{report.title}' diubah menjadi {report.get_status_display()}.") # Poin 8
        
        return redirect('main_app:home')