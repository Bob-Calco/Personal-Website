from django.shortcuts import render, redirect, HttpResponse
from django.template.loader import render_to_string
from datetime import datetime
from .forms import *
from .models import *
from .encryption import *

# Create your views here.

def home(request):
    context = {
        "title": "Home"
        }
    return render(request, "PW/home.html", context)

def app_overview(request):
    return render(request, "PW/app-overview.html", {})

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
                if form.cleaned_data['time1'] < form.cleaned_data['time2'] < form.cleaned_data['time3'] < form.cleaned_data['time4'] < form.cleaned_data['time5'] < form.cleaned_data['time6'] < form.cleaned_data['time7'] < form.cleaned_data['time8'] < form.cleaned_data['time9'] < form.cleaned_data['totalTime']:
                    form.save()
        return redirect('PW:memory')
    else:
        form = MemoryScoreForm()
        top_scores = memoryScore.objects.filter(date__gte=datetime(2017,2,1)).order_by('-score')[:30]
        return render(request, "PW/memory.html", {'form': form, 'top_scores': top_scores})

def encryption(request):
    if request.method == "POST":
        form = EncryptForm(request.POST)
        if form.is_valid():

            if form.cleaned_data['crypt'] == "encrypt":
                e = Encrypt(form.cleaned_data['text'])
                output = e.encrypt(form.cleaned_data['method'], form.keys())

            elif form.cleaned_data['crypt'] == "decrypt":
                d = Decrypt(form.cleaned_data['text'])
                keys = None

                if form.cleaned_data['method'] == 'caesar':
                    if form.cleaned_data['int_key1'] is not None:
                        keys = form.cleaned_data['int_key1']
                elif form.cleaned_data['method'] == 'affine':
                    if form.cleaned_data['int_key1'] is not None:
                        keys = [form.cleaned_data['int_key1'], None]
                    if form.cleaned_data['int_key2'] is not None:
                        if keys is None:
                            keys = [None, form.cleaned_data['int_key2']]
                        else:
                            keys[1] = form.cleaned_data['int_key2']

                output = sorted(d.decrypt(form.cleaned_data['method'], keys).items())

            context = {
                'crypt': form.cleaned_data['crypt'],
                'method': form.cleaned_data['method'],
                'output': output,
            }
            html = render_to_string("PW/encryptionAJAX.html", context)
            return HttpResponse(html)

        else:
            return redirect("PW:encryption")
    else:
        form = EncryptForm()
        return render(request, "PW/encryption.html", {'form': form})
