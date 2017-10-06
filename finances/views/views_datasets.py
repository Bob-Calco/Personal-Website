import finances.models as m
import finances.forms as f
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test

### SEARCH TERM DATASET VIEWS ###

@user_passes_test(lambda u: u.is_superuser)
def datasets(request):
    data = m.Datasets.objects.all()
    context = {
        'data': data
    }
    return render(request, "finances/datasets.html", context)

@user_passes_test(lambda u: u.is_superuser)
def dataset(request, pk=None):
    errors = False
    if request.method == "POST":
        if pk != None:
            form = f.DatasetForm(request.POST, instance=m.Datasets.objects.get(id=pk))
        else:
            form = f.DatasetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('finances:datasets')
        else:
            errors = True

    add = False if pk != None else True
    if errors == True:
        pass
    elif pk == None:
        form = f.DatasetForm()
    else:
        form = f.DatasetForm(instance=m.Datasets.objects.get(id=pk))

    context = {
        'form': form,
        'add': add,
    }
    return render(request, "finances/dataset.html", context)

@user_passes_test(lambda u: u.is_superuser)
def delete_dataset(request, pk):
    m.Datasets.objects.get(id=pk).delete()
    return redirect('finances:datasets')
