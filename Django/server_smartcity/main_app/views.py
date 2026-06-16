from django.shortcuts import redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Count, Q
from .models import Report


def visible_reports_for_user(user):
    if getattr(user, 'is_admin', False):
        return Report.objects.exclude(status='DRAFT')
    return Report.objects.filter(Q(status='DRAFT', reporter=user) | ~Q(status='DRAFT'))


class ReportListView(LoginRequiredMixin, ListView):
    model = Report
    template_name = 'main_app/home.html'
    context_object_name = 'reports'
    ordering = ['-pk']
    login_url = 'usermanagement_24782001:login'

    def get_queryset(self):
        query = self.request.GET.get('q')
        reports = visible_reports_for_user(self.request.user)

        if query:
            reports = reports.filter(
                Q(title__icontains=query) | Q(location__icontains=query)
            )

        return reports.order_by('-pk')


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard_24782001/index.html'
    login_url = 'usermanagement_24782001:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reports = visible_reports_for_user(self.request.user)

        context['status_data'] = reports.values('status').annotate(total=Count('status'))
        context['category_data'] = reports.values('category').annotate(total=Count('category'))

        context['total_reports'] = reports.count()
        context['pending_count'] = reports.filter(status='REPORTED').count()
        context['resolved_count'] = reports.filter(status='RESOLVED').count()

        context['recent_reports'] = reports.filter(status='REPORTED').order_by('-pk')[:5]

        return context


class ReportDetailView(LoginRequiredMixin, DetailView):
    model = Report
    template_name = 'main_app/report_detail.html'
    login_url = 'usermanagement_24782001:login'

    def get_queryset(self):
        return visible_reports_for_user(self.request.user)


class ReportCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Report
    fields = ['title', 'category', 'description', 'location']
    template_name = 'main_app/add_report.html'
    success_url = reverse_lazy('main_app:home')
    success_message = "Laporan berhasil ditambahkan ke Smartvillage Lite!"
    login_url = 'usermanagement_24782001:login'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_admin:
            messages.error(request, "Akses ditolak! Admin hanya boleh mengubah status laporan.")
            return redirect('main_app:home')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.reporter = self.request.user
        form.instance.status = 'REPORTED'
        return super().form_valid(form)


class ReportUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Report
    fields = ['title', 'category', 'description', 'location']
    template_name = 'main_app/add_report.html'
    success_url = reverse_lazy('main_app:home')
    success_message = "Data laporan berhasil diupdate!"
    login_url = 'usermanagement_24782001:login'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_admin:
            messages.error(request, "Admin tidak boleh mengedit isi laporan Citizen.")
            return redirect('main_app:home')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Report.objects.filter(reporter=self.request.user)


class ReportDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Report
    template_name = 'main_app/report_confirm_delete.html'
    success_url = reverse_lazy('main_app:home')
    success_message = "Laporan telah dihapus dari sistem."
    login_url = 'usermanagement_24782001:login'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_admin:
            messages.error(request, "Admin tidak boleh menghapus laporan Citizen.")
            return redirect('main_app:home')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Report.objects.filter(reporter=self.request.user)


class ReportUpdateStatusView(LoginRequiredMixin, View):
    login_url = 'usermanagement_24782001:login'

    def post(self, request, pk):
        if not request.user.is_admin:
            return redirect('main_app:home')

        report = get_object_or_404(Report.objects.exclude(status='DRAFT'), pk=pk)

        if report.status == 'REPORTED':
            report.status = 'VERIFIED'
        elif report.status == 'VERIFIED':
            report.status = 'IN_PROGRESS'
        elif report.status == 'IN_PROGRESS':
            report.status = 'RESOLVED'

        report.save()
        messages.success(request, f"Status '{report.title}' diperbarui.")
        return redirect('main_app:home')