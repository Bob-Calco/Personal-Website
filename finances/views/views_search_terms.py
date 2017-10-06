import json
import finances.models as m
import finances.forms as f
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test

import finances.database as db

### SEARCH TERMS VIEWS ###

@user_passes_test(lambda u: u.is_superuser)
def search_terms(request):
    data = m.SearchTerms.objects.all()
    context = {
        'data': data,
    }
    return render(request, "finances/search-terms.html", context)

@user_passes_test(lambda u: u.is_superuser)
def search_term(request, pk=None):
    errors = False
    if request.method == "POST":
        if pk != None:
            form = f.SearchTermForm(request.POST, instance=m.SearchTerms.objects.get(id=pk))
        else:
            form = f.SearchTermForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('finances:search_terms')
        else:
            errors = True

    category_data = json.dumps(db.categories())
    add = False if pk != None else True
    if errors == True:
        pass
    elif pk == None:
        form = f.SearchTermForm()
    else:
        form = f.SearchTermForm(instance=m.SearchTerms.objects.get(id=pk))

    context = {
        'category_data': category_data,
        'form': form,
        'add': add,
    }
    return render(request, "finances/search-term.html", context)

@user_passes_test(lambda u: u.is_superuser)
def delete_search_term(request, pk):
    m.SearchTerms.objects.get(id=pk).delete()
    return redirect('finances:search_terms')
