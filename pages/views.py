from django.views import generic


class AboutView(generic.TemplateView):
    template_name = 'pages/about.html'


class StatusView(generic.TemplateView):
    template_name = 'pages/status.html'
