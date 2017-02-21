from django.shortcuts import render, redirect
import groceries.forms as f
import groceries.models as m

# Create your views here.
from django.http import HttpResponse

def home(request):
    if request.method == "POST":
        form = f.ItemForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('groceries:home')
    else:
        form = f.ItemForm
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
    items = m.Items.objects.filter(recipe=number)
    context = {
        "recipe": recipe,
        "items": items,
    }
    return render(request, "groceries/recipe.html", context)

def recipeEdit(request, number):
    recipe = m.Recipes.objects.filter(id=number)[0]
    items = m.Items.objects.filter(recipe=number)

    if request.method == "POST":
        recipeForm = f.RecipeForm(instance=recipe, data=request.POST, prefix="recipe")
        itemFormSet = f.ItemFormSet(queryset=items, data=request.POST, prefix="item")
        print(recipeForm.is_valid())
        print(itemFormSet.is_valid())
        if recipeForm.is_valid() and itemFormSet.is_valid():
            r = recipeForm.save()
            for form in itemFormSet:
                a = form.save(commit=False)
                a.recipe = r
                a.save()
            return redirect('groceries:recipes')
        return redirect('groceries:home')
    else:
        recipeForm = f.RecipeForm(prefix="recipe", instance=recipe)
        itemFormSet = f.ItemFormSet(prefix="item", queryset=items)
        context = {
            "recipeForm": recipeForm,
            "itemFormSet": itemFormSet,
        }
        return render(request, "groceries/recipe-edit.html", context)

def makeList(request):
    return HttpResponse("Here you'll be able to make a new grocery list")

def groceryList(request):
    return HttpResponse("Here you can check off the items on the list")
