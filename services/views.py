from django.views.generic import TemplateView


class ServiceListView(TemplateView):
    template_name = 'base.html'
