from django.shortcuts import render
from .forms import AddedForm

# Create your views here.
from django.http import HttpResponse

def home(request):
    if request.method == "POST":
        form = AddedForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('groceries:home.html')
    else:
        form = AddedForm
        context = {
            "title": "Home",
            "form": form,
            }
        return render(request, "groceries/home.html", context)

def recipes(request):
    return HttpResponse("Here there will be a list of recipes")

def recipe(request):
    return HttpResponse("Here you will find a single recipe")

def makeList(request):
    return HttpResponse("Here you'll be able to make a new grocery list")

def groceryList(request):
    return HttpResponse("Here you can check off the items on the list")
