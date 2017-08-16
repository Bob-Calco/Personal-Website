from django.conf.urls import url
from django.views.generic import TemplateView

app_name = 'projectsunset'
urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='projectsunset/home.html')),
]
