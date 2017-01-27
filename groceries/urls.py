from django.conf.urls import url

from . import views

app_name = 'groceries'
urlpatterns = [
  url(r'^$', views.home, name="home"),
  url(r'^recipes/', views.recipes, name="recipes"),
  url(r'^recipe/adf', views.recipe, name="recipe"),
  url(r'^makeList/', views.makeList, name="makeList"),
  url(r'^groceryList/', views.groceryList, name="groceryList"),
]
