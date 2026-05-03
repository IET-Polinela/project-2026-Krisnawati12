from django.views.generic import TemplateView
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q
from django.contrib.auth.mixins import LoginRequiredMixin
from main_app.models import Report # Mengambil model dari app utama

# 1. View Utama Dashboard (Class-Based View)
# Mengatur halaman index dan data ringkasan untuk tabel
class DashboardView(LoginRequiredMixin, TemplateView):
    # Gunakan folder 'dashboard/index.html' sesuai struktur templates app
    template_name = 'dashboard/index.html'
    login_url = 'usermanagement_24782001:login' # Arahkan ke login jika belum masuk

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Menampilkan 5 laporan terbaru dengan status REPORTED
        context['recent_reports'] = Report.objects.filter(status='REPORTED').order_by('-id')[:5]
        # Menampilkan 5 laporan terbaru yang sudah RESOLVED (Selesai)
        context['resolved_reports'] = Report.objects.filter(status='RESOLVED').order_by('-id')[:5]
        
        # Summary tambahan untuk kartu dashboard (opsional tapi bagus untuk visual)
        context['total_reports'] = Report.objects.count()
        return context

# 2. API untuk data Chart.js (JSON)
# Menyediakan data statistik untuk grafik secara asinkron
def report_stats_api(request):
    # Agregasi data menggunakan Count dari Django ORM
    status_stats = Report.objects.values('status').annotate(total=Count('status'))
    category_stats = Report.objects.values('category').annotate(total=Count('category'))

    data = {
        'status_labels': [s['status'] for s in status_stats],
        'status_data': [s['total'] for s in status_stats],
        'category_labels': [c['category'] for c in category_stats],
        'category_data': [c['total'] for c in category_stats],
    }
    return JsonResponse(data)

# 3. API untuk Live Search (JSON)
# Mendukung pencarian instan berdasarkan judul atau lokasi
def report_search_api(request):
    query = request.GET.get('q', '')
    if query:
        # Gunakan Q untuk mencari di judul ATAU lokasi (icontains = case-insensitive)
        reports = Report.objects.filter(
            Q(title__icontains=query) | Q(location__icontains=query)
        )[:10]
    else:
        reports = []

    results = [{
        'id': r.id, 
        'title': r.title, 
        'category': r.category, 
        'status': r.status,
        'location': r.location
    } for r in reports]
    
    return JsonResponse({'reports': results})

# 4. API untuk Detail Modal (JSON)
# Mengambil data rinci untuk ditampilkan di jendela Pop-up
def report_detail_api(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    data = {
        'title': report.title,
        'category': report.category,
        'description': report.description,
        'location': report.location,
        'status': report.status,
    }
    return JsonResponse(data)