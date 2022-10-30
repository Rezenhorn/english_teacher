from django.views.generic.base import TemplateView


class AboutAuthorView(TemplateView):
    template_name = 'about/about_me.html'


class IndexView(TemplateView):
    template_name = 'about/index.html'