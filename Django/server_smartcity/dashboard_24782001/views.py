from django.views.generic import TemplateView
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from main_app.models import Report


def visible_reports_for_user(user):
    if getattr(user, 'is_admin', False):
        return Report.objects.exclude(status='DRAFT')
    return Report.objects.filter(Q(status='DRAFT', reporter=user) | ~Q(status='DRAFT'))


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/index.html'
    login_url = 'usermanagement_24782001:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reports = visible_reports_for_user(self.request.user)

        context['recent_reports'] = reports.filter(status='REPORTED').order_by('-id')[:5]
        context['resolved_reports'] = reports.filter(status='RESOLVED').order_by('-id')[:5]
        context['total_reports'] = reports.count()

        return context


@login_required(login_url='usermanagement_24782001:login')
def report_stats_api(request):
    reports = visible_reports_for_user(request.user)
    status_stats = reports.values('status').annotate(total=Count('status'))
    category_stats = reports.values('category').annotate(total=Count('category'))

    data = {
        'status_labels': [s['status'] for s in status_stats],
        'status_data': [s['total'] for s in status_stats],
        'category_labels': [c['category'] for c in category_stats],
        'category_data': [c['total'] for c in category_stats],
    }
    return JsonResponse(data)


@login_required(login_url='usermanagement_24782001:login')
def report_search_api(request):
    query = request.GET.get('q', '')

    if query:
        reports = visible_reports_for_user(request.user).filter(
            Q(title__icontains=query) | Q(location__icontains=query)
        )[:10]
    else:
        reports = []

    results = [{
        'id': r.id,
        'title': r.title,
        'category': r.category,
        'status': r.status,
        'location': r.location,
    } for r in reports]

    return JsonResponse({'reports': results})


@login_required(login_url='usermanagement_24782001:login')
def report_detail_api(request, report_id):
    report = get_object_or_404(visible_reports_for_user(request.user), id=report_id)

    data = {
        'title': report.title,
        'category': report.category,
        'description': report.description,
        'location': report.location,
        'status': report.status,
    }
    return JsonResponse(data)