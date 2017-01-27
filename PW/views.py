from django.shortcuts import render, redirect
from .forms import MemoryScoreForm
from .models import memoryScore

# Create your views here.

def home(request):
    context = {
        "title": "Home"
        }
    return render(request, "PW/home.html", context)

def about(request):
    context = {
        "title": "About"
        }
    return render(request, "PW/about.html", context)

def projects(request):
    context = {
        "title": "Projects"
        }
    return render(request, "PW/projects.html", context)

def memory(request):
    if request.method == "POST":
        form = MemoryScoreForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['totalTime'] > 10 or form.cleaned_data['turns'] > 10:
                if form.time1 < form.time2 < form.time3 < form.time4 < form.time5 < form.time6 < form.time7 < form.time8 < form.time9 < form.totalTime:
                    form.save()
        return redirect('PW:memory')
    else:
        form = MemoryScoreForm()
        top_scores = memoryScore.objects.order_by('-score')[:30]
        return render(request, "PW/memory.html", {'form': form, 'top_scores': top_scores})
