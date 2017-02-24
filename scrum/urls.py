from django.conf.urls import url

from . import views

app_name = 'scrum'
urlpatterns = [
    url(r'^$', views.product_backlog, name='product-backlog'),
    url(r'^add-userstory/$', views.add_userstory, name='add-userstory'),
    url(r'^add-epic/$', views.add_epic, name='add-epic'),
]
