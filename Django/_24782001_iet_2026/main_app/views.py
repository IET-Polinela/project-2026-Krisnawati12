from django.shortcuts import render, redirect, get_object_or_404
from .models import Report
from .forms import ReportForm

# READ: Lihat semua data di home.html
def home(request):
    reports = Report.objects.all()
    return render(request, 'main_app/home.html', {'reports': reports})

# CREATE: Tambah data laporan
def add_report(request):
    if request.method == "POST":
        form = ReportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main_app:home')
    else:
        form = ReportForm()
    return render(request, 'main_app/add_report.html', {'form': form})

# UPDATE: Edit data
def update_report(request, pk):
    report = get_object_or_404(Report, pk=pk)
    if request.method == "POST":
        form = ReportForm(request.POST, instance=report)
        if form.is_valid():
            form.save()
            return redirect('main_app:home')
    else:
        form = ReportForm(instance=report)
    return render(request, 'main_app/add_report.html', {'form': form})

# DELETE: Hapus data
def delete_report(request, pk):
    report = get_object_or_404(Report, pk=pk)
    if request.method == "POST":
        report.delete()
        return redirect('main_app:home')
    return render(request, 'main_app/report_confirm_delete.html', {'report': report})