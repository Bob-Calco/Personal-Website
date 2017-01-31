from django.shortcuts import render
import groceries.forms as f
import groceries.models as m

# Create your views here.
from django.http import HttpResponse

def home(request):
    if request.method == "POST":
        form = f.AddedForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('groceries:home.html')
    else:
        form = f.AddedForm
        context = {
            "title": "Home",
            "form": form,
            }
        return render(request, "groceries/home.html", context)

def recipes(request):
    recipes = m.Recipes.objects.all()
    context = {
        "title": "Recipes",
        "recipes": recipes,
    }
    return render(request, "groceries/recipes.html", context)

def recipe(request, number):
    recipe = m.Recipes.objects.filter(id=number)[0]
    ingredients = m.RecipeIngredients.objects.filter(recipe=recipe)
    context = {
        "recipe": recipe,
        "ingredients": ingredients
    }
    return render(request, "groceries/recipe.html", context)

def recipeEdit(request, number):
    recipeForm = f.RecipeForm(prefix="recipe")
    ingredientFormSet = f.IngredientFormSet(prefix="ingredient")
    tagFormSet = f.TagFormSet(prefix="tag")
    context = {
        "recipeForm": recipeForm,
        "ingredientFormSet": ingredientFormSet,
        "tagFormSet": tagFormSet,
    }
    return render(request, "groceries/recipe-edit.html", context)

def newRecipe(request):
    form = f.RecipeForm
    context = {
        "form": form,
    }
    return render(request, "groceries/recipe-edit.html", context)

def makeList(request):
    return HttpResponse("Here you'll be able to make a new grocery list")

def groceryList(request):
    return HttpResponse("Here you can check off the items on the list")
