from django.shortcuts import render, redirect
from .forms import MemoryScoreForm
from .models import memoryScore

# Create your views here.

def home(request):
    context = {
        "title": "Home"
        }
    return render(request, "home.html", context)

def about(request):
    context = {
        "title": "About"
        }
    return render(request, "about.html", context)

def projects(request):
    context = {
        "title": "Projects"
        }
    return render(request, "projects.html", context)

def memory(request):
    if request.method == "POST":
        form = MemoryScoreForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['time'] > 10 or form.cleaned_data['turns'] > 10:
                form.save()
        return redirect('memory')
    else:
        form = MemoryScoreForm()
        top_scores = memoryScore.objects.order_by('-score')[:30]
        return render(request, "memory.html", {'form': form, 'top_scores': top_scores})