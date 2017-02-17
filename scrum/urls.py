from django.conf.urls import url

from . import views

app_name = 'scrum'
urlpatterns = [
    url(r'^$', views.product_backlog, name='product-backlog'),
]
