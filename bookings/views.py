from django.views.generic import TemplateView


class BookingDashboardView(TemplateView):
    template_name = 'base.html'
