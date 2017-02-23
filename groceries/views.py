from django.shortcuts import render, redirect, HttpResponse
import groceries.forms as f
import groceries.models as m
from django.db.models import Q

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
            if request.POST.get("save"):
                recipeForm.save()
                itemFormSet.save()
            if request.POST.get("delete"):
                recipe.delete()
            return redirect('groceries:recipe', number)
        return redirect('groceries:home')
    else:
        recipeForm = f.RecipeForm(prefix="recipe", instance=recipe)
        itemFormSet = f.ItemFormSet(prefix="item", instance=recipe)
        context = {
            "title": "Edit",
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
                return redirect('groceries:recipe', r.id)
        print(recipeForm.errors)
        print(itemFormSet.errors)
        return redirect('groceries:home')
    else:
        recipeForm = f.RecipeForm(prefix="recipe")
        itemFormSet = f.ItemFormSet(queryset=m.Items.objects.none(), prefix="item")
        context = {
            "title": "New",
            "recipeForm": recipeForm,
            "itemFormSet": itemFormSet,
        }
        return render(request, "groceries/recipe-edit.html", context)

def makeGroceryList(request):
    if request.method == "POST":
        recipe_ids = request.POST['recipes'].split(',')[1:]
        recipes = m.Recipes.objects.filter(id__in=recipe_ids)
        items = m.Items.objects.filter(recipe=None).filter(status=0)
        groceryList = m.GroceryLists()
        groceryList.save()
        for item in items:
            groceryList.items.add(item)
        for recipe in recipes:
            groceryList.recipes.add(recipe)
        return redirect('groceries:groceryList')
    else:
        extra_items = m.Items.objects.filter(recipe=None).filter(status=0)
        preselected_recipes = m.Recipes.objects.order_by('dateLastUsed')[:2]
        all_recipes = m.Recipes.objects.exclude(id__in=[preselected_recipes[0].id, preselected_recipes[1].id])
        added_form = f.ItemForm
        context = {
            "extra_items": extra_items,
            "all_recipes": all_recipes,
            "added_form": added_form,
            "preselected_recipes": preselected_recipes,
        }
        return render(request, "groceries/make-grocery-list.html", context)

def addItem(request):
    if request.method == "POST":
        form = f.ItemForm(request.POST)
        if form.is_valid():
            item = form.save()
            html = item.description
            return HttpResponse(html)

def groceryList(request):
    extra_items = m.GroceryLists.objects.latest('date').items.all()
    recipes = m.GroceryLists.objects.latest('date').recipes.all()
    recipe_items = m.Items.objects.filter( Q(recipe=recipes[0]) | Q(recipe=recipes[1]) )
    context = {
        "extra_items": extra_items,
        "recipe_items": recipe_items,
    }
    return render(request, "groceries/grocery-list.html", context)
