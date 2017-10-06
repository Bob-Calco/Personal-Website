import finances.models as m
import finances.forms as f
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import user_passes_test

### CATEGORIES VIEWS ###

@user_passes_test(lambda u: u.is_superuser)
def categories(request):
    categories = m.Categories.objects.filter(specification_of__isnull=True)
    context = {
        'categories': categories,
    }
    return render(request, "finances/categories.html", context)

@user_passes_test(lambda u: u.is_superuser)
def category(request, number):
    if request.method == 'POST':
        form = f.CategoryForm(request.POST, instance=m.Categories.objects.get(id=number))
        if form.is_valid():
            category = form.save()
            html = render_to_string("finances/category-cell.html", {'category': category, 'is_income': is_income})
            return JsonResponse({'saved': True, 'html': html, 'add': False })
    else:
        form = f.CategoryForm(instance=m.Categories.objects.get(id=number))
    context = {
        'form': form,
        'add': False,
        'specification_of': True if form.instance.specification_of is not None else False,
    }
    html = render_to_string("finances/category.html", context, request=request)
    return JsonResponse({'saved': False, 'html': html})

@user_passes_test(lambda u: u.is_superuser)
def add_category(request, is_income, specification_of=None):
    if request.method == 'POST':
        form = f.CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            html = render_to_string("finances/category-cell.html", {'category': category, 'is_income': int(category.is_income)})
            if category.specification_of is not None:
                specification_of = int(category.specification_of.id)
            else:
                specification_of = None
            return JsonResponse({'saved': True, 'html': html, 'add': True, 'is_income': int(category.is_income), 'specification_of': specification_of})
    else:
        form = f.CategoryForm(initial={'is_income': True if is_income == '1' else False, 'specification_of': specification_of})
    context = {
        'form': form,
        'add': True,
        'is_income': is_income,
        'specification_of': specification_of,
    }
    html = render_to_string("finances/category.html", context, request=request)
    return JsonResponse({'saved': False, 'html': html, 'is_income': is_income, 'specification_of': specification_of})

@user_passes_test(lambda u: u.is_superuser)
def delete_category(request, number):
    m.Categories.objects.get(id=number).delete()
    return redirect('finances:categories')
