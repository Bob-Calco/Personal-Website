from django.conf.urls import url

from . import views

app_name = 'groceries'
urlpatterns = [
  url(r'^$', views.home, name="home"),
  url(r'^recipes/$', views.recipes, name="recipes"),
  url(r'^recipes/export/$', views.exportRecipes, name="exportRecipes"),
  url(r'^recipes/import/$', views.importRecipes, name ="importRecipes"),
  url(r'^recipe/(?P<number>[0-9]+)/$', views.recipe, name="recipe"),
  url(r'^recipe/(?P<number>[0-9]+)/edit/$', views.recipeEdit, name="recipeEdit"),
  url(r'^recipe/new/$', views.recipeNew, name="recipeNew"),
  url(r'^grocery-list/$', views.groceryList, name="groceryList"),
  url(r'^grocery-list/make/$', views.makeGroceryList, name="makeGroceryList"),
  url(r'^grocery-list/make/add-item/$', views.addItem, name="addItemAjax"),
]
