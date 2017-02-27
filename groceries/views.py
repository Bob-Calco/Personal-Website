from django.shortcuts import render, redirect, HttpResponse
import groceries.forms as f
import groceries.models as m
from django.db.models import Q
from django.utils import timezone
from django.db.models.base import ObjectDoesNotExist
import xml.etree.ElementTree as ET
from wsgiref.util import FileWrapper

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

def exportRecipes(request):
    recipes = m.Recipes.objects.all()
    root = ET.Element("recipes")

    for recipe in recipes:
        ele = ET.SubElement(root, "recipe")
        ET.SubElement(ele, "name").text = recipe.name
        ET.SubElement(ele, "howto").text = recipe.howto
        items = ET.SubElement(ele, "items")
        for item in recipe.items_set.all():
            ET.SubElement(items, "item").text = item.description

    tree = ET.ElementTree(root)
    response = HttpResponse(ET.tostring(root, encoding='utf8', method ='xml'), content_type='application/xml')
    response['Content-Disposition'] = 'attachment; filename=recipe-export.xml'
    return response

def importRecipes(request):
    if request.method == "POST" and request.FILES['xml']:
        xml = ET.parse(request.FILES['xml'])
        root = xml.getroot()
        m.Recipes.objects.all().delete()
        for recipe in root:
            r = m.Recipes()
            r.name = recipe[0].text
            r.howto = recipe[1].text
            r.save()
            for item in recipe[2]:
                i = m.Items()
                i.description = item.text
                i.recipe = r
                i.save()
        return redirect('groceries:recipes')
    else:
        return redirect('groceries:home')


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
    try:
        recent_list = m.GroceryLists.objects.latest('date')
    except ObjectDoesNotExist:
        return redirect('groceries:makeGroceryList')
    if recent_list.finished == False:
        if request.method == "POST":
            recent_list.finished = True
            recent_list.items.all().status = 1
            recent_list.recipes.all().dateLastUsed = timezone.now()
            recent_list.save()
            return redirect("groceries:home")
        else:
            extra_items = recent_list.items.all()
            recipes = recent_list.recipes.all()
            recipe_items = m.Items.objects.filter(recipe__in=recipes)
            context = {
                "extra_items": extra_items,
                "recipe_items": recipe_items,
            }
            return render(request, "groceries/grocery-list.html", context)
    else:
        return redirect('groceries:makeGroceryList')
