import groceries.forms as f
import groceries.models as m
import xml.etree.ElementTree as ET
from django.db.models import Q
from django.db.models.base import ObjectDoesNotExist
from django.utils import timezone
from django.shortcuts import render, redirect, HttpResponse
from wsgiref.util import FileWrapper
from django.core import serializers
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    # A post to this page is an extra item, so add that thing
    if request.method == "POST":
        form = f.ItemForm(request.POST)
        if form.is_valid():
            model = form.save(commit=False)
            model.user = request.USER
            model.save()
        return redirect('groceries:home')
    else:
    # GET request context
        form = f.ItemForm
        context = {
            "title": "Home",
            "form": form,
            }
        return render(request, "groceries/home.html", context)

@login_required
def recipes(request):
    # GET request, load all the recipes
    recipes = m.Recipes.objects.filter(user=request.USER)
    context = {
        "title": "Recipes",
        "recipes": recipes,
    }
    return render(request, "groceries/recipes.html", context)

@login_required
def exportRecipes(request):
    # load all the recipes and create the XML tree root
    recipes = m.Recipes.objects.filter(user=request.USER)
    root = ET.Element("recipes")

    # add information for every recipe
    for recipe in recipes:
        ele = ET.SubElement(root, "recipe")
        ET.SubElement(ele, "name").text = recipe.name
        ET.SubElement(ele, "howto").text = recipe.howto
        items = ET.SubElement(ele, "items")
        for item in recipe.items_set.all():
            ET.SubElement(items, "item").text = item.description

    # send it back as a download
    tree = ET.ElementTree(root)
    response = HttpResponse(ET.tostring(root, encoding='utf8', method ='xml'), content_type='application/xml')
    response['Content-Disposition'] = 'attachment; filename=recipe-export.xml'
    return response

@login_required
def importRecipes(request):
    # We need a post request with an XML file
    if request.method == "POST" and request.FILES['xml']:
        xml = ET.parse(request.FILES['xml'])
        root = xml.getroot()

        # Empty the current list of recipes
        m.Recipes.objects.filter(user=request.USER).delete()

        # Save all the new recipes
        for recipe in root:
            r = m.Recipes()
            r.name = recipe[0].text
            r.howto = recipe[1].text
            r_model = r.save(commit=False)
            r_model.user = request.USER
            r_model.save()
            for item in recipe[2]:
                i = m.Items()
                i.description = item.text
                i.recipe = r
                i_model = i.save(commit=False)
                i_model.user = request.USER
                i_model.save()
        return redirect('groceries:recipes')
    else:
        return redirect('groceries:home')

@login_required
def recipe(request, number):
    # GET request, get the context
    recipe = m.Recipes.objects.filter(user=request.USER).filter(id=number)[0]
    items = m.Items.objects.filter(user=request.USER).filter(recipe=number)
    context = {
        "recipe": recipe,
        "items": items,
    }
    return render(request, "groceries/recipe.html", context)

@login_required
def recipeEdit(request, number):
    # Load the recipe and its items
    recipe = m.Recipes.objects.filter(user=request.USER).filter(id=number)[0]
    items = m.Items.objects.filter(user=request.USER).filter(recipe=number)

    # do something if it is a POST
    if request.method == "POST":
        recipeForm = f.RecipeForm(instance=recipe, data=request.POST, prefix="recipe")
        itemFormSet = f.ItemFormSet(instance=recipe, data=request.POST, prefix="item")
        if recipeForm.is_valid() and itemFormSet.is_valid():
            # Update recipe
            if request.POST.get("save"):
                r_model = recipeForm.save(commit=False)
                r_model.user = request.USER
                r_model.save()
                i_model = itemFormSet.save(commit=False)
                i_model.user = request.USER
                i_model.save()
                return redirect('groceries:recipe', number)
            # Delete recipe
            if request.POST.get("delete"):
                recipe.delete()
                return redirect('groceries:recipes')
        return redirect('groceries:home')
    # GET request, load context
    else:
        recipeForm = f.RecipeForm(prefix="recipe", instance=recipe)
        itemFormSet = f.ItemFormSet(prefix="item", instance=recipe)
        context = {
            "title": "Edit",
            "recipeForm": recipeForm,
            "itemFormSet": itemFormSet,
        }
        return render(request, "groceries/recipe-edit.html", context)

@login_required
def recipeNew(request):
    # POST request, save the new recipe
    if request.method == "POST":
        recipeForm = f.RecipeForm(request.POST, prefix="recipe")
        if recipeForm.is_valid():
            # Don't yet go to the database, first we need to check the itemformset
            r = recipeForm.save(commit=False)
            itemFormSet = f.ItemFormSet(request.POST, instance=r, prefix="item")
            if itemFormSet.is_valid():
                # now we can save
                r.user = request.USER
                r.save()
                i = itemFormSet.save(commit=False)
                i.user = request.USER
                i.save()
                return redirect('groceries:recipe', r.id)
        return redirect('groceries:home')
    # GET request, load the context
    else:
        recipeForm = f.RecipeForm(prefix="recipe")
        itemFormSet = f.ItemFormSet(queryset=m.Items.objects.none(), prefix="item")
        context = {
            "title": "New",
            "recipeForm": recipeForm,
            "itemFormSet": itemFormSet,
        }
        return render(request, "groceries/recipe-edit.html", context)

@login_required
def makeGroceryList(request):
    # POST request, create grocery list
    if request.method == "POST":
        recipe_ids = request.POST['recipes'].split(',')[1:]
        recipes = m.Recipes.objects.filter(user=request.USER).filter(id__in=recipe_ids)
        items = m.Items.objects.filter(user=request.USER).filter(recipe=None).filter(status=0)
        groceryList = m.GroceryLists()
        g = groceryList.save(commit=False)
        g.user = request.USER
        g.save()
        for item in items:
            groceryList.items.add(item)
        for recipe in recipes:
            groceryList.recipes.add(recipe)
        return redirect('groceries:groceryList')
    # GET request, load things, select the two longest not used recipes
    else:
        extra_items = m.Items.objects.filter(user=request.USER).filter(recipe=None).filter(status=0)
        preselected_recipes = m.Recipes.objects.filter(user=request.USER).order_by('dateLastUsed')[:2]
        all_recipes = m.Recipes.objects.filter(user=request.USER).exclude(id__in=[preselected_recipes[0].id, preselected_recipes[1].id])
        added_form = f.ItemForm()
        context = {
            "extra_items": extra_items,
            "all_recipes": all_recipes,
            "added_form": added_form,
            "preselected_recipes": preselected_recipes,
        }
        return render(request, "groceries/make-grocery-list.html", context)

@login_required
def addItem(request):
    # POST request, add item
    if request.method == "POST":
        form = f.ItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.USER
            item.save()
            data = serializers.serialize("json", [item,])

            # add item to the current grocery list if it exists
            try:
                recent_list = m.GroceryLists.objects.filter(user=request.USER).latest('date')
            except ObjectDoesNotExist:
                return HttpResponse(data, content_type='application/json')
            if recent_list.finished == False:
                recent_list.items.add(item)

            return HttpResponse(data, content_type='application/json')

@login_required
def groceryList(request):
    # check if there is a current grocery list
    try:
        recent_list = m.GroceryLists.objects.filter(user=request.USER).latest('date')
    except ObjectDoesNotExist:
        return redirect('groceries:makeGroceryList')
    if recent_list.finished == False:
        # If it is a post to this page we need to close off the current list
        if request.method == "POST":
            recent_list.finished = True
            recent_list.items.all().status = 1
            recent_list.recipes.all().dateLastUsed = timezone.now()
            recent_list.save()
            return redirect("groceries:home")
        # Otherwise we will show the current list
        else:
            extra_items = recent_list.items.all()
            recipes = recent_list.recipes.all()
            recipe_items = m.Items.objects.filter(recipe__in=recipes)
            added_form = f.ItemForm()
            context = {
                "extra_items": extra_items,
                "recipe_items": recipe_items,
                "added_form": added_form,
            }
            return render(request, "groceries/grocery-list.html", context)
    # If there is no current list we need to go to the page to make one
    else:
        return redirect('groceries:makeGroceryList')

@login_required
def cooking(request):
    try:
        recent_list = m.GroceryLists.objects.filter(user=request.USER).latest('date')
    except ObjectDoesNotExist:
        return redirect('groceries:makeGroceryList')

    context = {"recent_list": recent_list }
    return render(request, "groceries/cooking.html", context)

@login_required
def extraItems(request):
    extra_items = m.Items.objects.filter(user=request.USER).filter(status=0).filter(recipe=None)
    context = {"extra_items": extra_items }
    return render(request, "groceries/extra-items.html", context)
