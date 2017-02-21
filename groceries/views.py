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
        itemFormSet = f.ItemFormSet(instance=recipe, data=request.POST, prefix="item")
        if recipeForm.is_valid() and itemFormSet.is_valid():
            recipeForm.save()
            itemFormSet.save()
            return redirect('groceries:recipes')
        return redirect('groceries:home')
    else:
        recipeForm = f.RecipeForm(prefix="recipe", instance=recipe)
        itemFormSet = f.ItemFormSet(prefix="item", instance=recipe)
        context = {
            "recipeForm": recipeForm,
            "itemFormSet": itemFormSet,
        }
        return render(request, "groceries/recipe-edit.html", context)

def recipeNew(request):
    if request.method == "POST":
        recipeForm = f.RecipeForm(request.POST, prefix="recipe")
        if recipeForm.is_valid():
            r = recipeForm.save(commit=False)
            itemFormSet = f.ItemFormSet(request.POST, instance=r, prefix="item")
            if itemFormSet.is_valid():
                recipeForm.save()
                itemFormSet.save()
                return redirect('groceries:recipes')
        return redirect('groceries:home')
    else:
        recipeForm = f.RecipeForm(prefix="recipe")
        itemFormSet = f.ItemFormSet(queryset=m.Items.objects.none(), prefix="item")
        context = {
            "recipeForm": recipeForm,
            "itemFormSet": itemFormSet,
        }
        return render(request, "groceries/recipe-edit.html", context)

def groceryList(request):
    recipes = m.Recipes.objects.order_by('dateLastUsed')[:2]
    recipe1 = m.Items.objects.filter(recipe=recipes[0])
    recipe2 = m.Items.objects.filter(recipe=recipes[1])
    extra_items = m.Items.objects.filter(recipe=None)
    context = {
        "recipe1": recipe1,
        "recipe2": recipe2,
        "extra_items": extra_items,
    }
    return render(request, "groceries/grocery-list.html", context)
