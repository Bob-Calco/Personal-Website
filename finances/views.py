import json
import finances.models as m
import finances.forms as f
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from django.core import serializers
from datetime import date

@user_passes_test(lambda u: u.is_superuser)
def home(request):
    context = None
    return render(request, "finances/home.html", context)

### TRANSACTION VIEWS ###

@user_passes_test(lambda u: u.is_superuser)
def transactions(request, year=date.today().year, month=date.today().month):
    year = int(year)
    month = int(month)
    if request.method =="GET":
        if month == 12:
            end = date(year+1, 1,1)
        else:
            end = date(year, month+1,1)
        transactions = m.Transactions.objects.filter(date__gte=date(year,month,1)).filter(date__lt=end).order_by('date')
        context = {
            "transactions": transactions,
            "year": year,
            "month": month,
        }
        return render(request, "finances/transactions.html", context)

@user_passes_test(lambda u: u.is_superuser)
def transaction(request, number=None):
    errors = False
    if request.method == "POST":
        if number != None:
            transaction = m.Transactions.objects.get(id=number)
            form = f.TransactionForm(request.POST, instance=transaction)
        else:
            form = f.TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('finances:transactions')
        else:
            errors = True

    category_data = {}
    categories = m.Categories.objects.filter(specification_of__isnull=True)
    for category in categories:
        specifications = m.Categories.objects.filter(specification_of__isnull=False).filter(specification_of=category)
        category_data[category.name] = []
        for specification in specifications:
            category_data[category.name].append(specification.name)
    category_data = json.dumps(category_data)

    add = False if number != None else True

    if errors == True:
        pass
    elif number != None:
        transaction = m.Transactions.objects.get(id=number)
        form = f.TransactionForm(instance=transaction)
    else:
        form = f.TransactionForm()
    context = {
        "form": form,
        "category_data": category_data,
        "add": add,
    }
    return render(request, "finances/transaction.html", context)

@user_passes_test(lambda u: u.is_superuser)
def delete_transaction(request, number):
    m.Transactions.objects.get(id=number).delete()
    return redirect('finances:transactions')

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
    errors = False
    if request.method == 'POST':
        form = f.CategoryForm(request.POST, instance=m.Categories.objects.get(id=number))
        if form.is_valid():
            form.save()
            return redirect('finances:categories')
        else:
            errors = True
    if errors == False:
        form = f.CategoryForm(instance=m.Categories.objects.get(id=number))
    context = {
        'form': form,
        'add': False
    }
    return render(request, "finances/category.html", context)

@user_passes_test(lambda u: u.is_superuser)
def add_category(request, is_income, specification_of=None):
    errors = False
    if request.method == 'POST':
        form = f.CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('finances:categories')
        else:
            errors = True
    is_income = True if is_income == '1' else False
    if errors == False:
        form = f.CategoryForm(initial={'is_income': is_income, 'specification_of': specification_of})
    context = {
        'form': form,
        'add': True
    }
    return render(request, "finances/category.html", context)

@user_passes_test(lambda u: u.is_superuser)
def delete_category(request, number):
    m.Categories.objects.get(id=number).delete()
    return redirect('finances:categories')

### BALANCE VIEWS ###

@user_passes_test(lambda u: u.is_superuser)
def balance(request, year=date.today().year):
    balances = m.Balances.objects.filter(date)
    context = {
        'balances': balances
    }
    return render(request, "finances/balance.html", context)

### SEARCh TERMS VIEWS ###

@user_passes_test(lambda u: u.is_superuser)
def search_terms(request):
    context = None
    return render(request, "finances/home.html", context)

'''
category_data = {'income': {}, 'expense': {}}
categories = m.Categories.objects.filter(specification_of__isnull=True)
for category in categories:
    specifications = m.Categories.objects.filter(specification_of__isnull=False).filter(specification_of=category)
    if category.is_income == True:
        category_data['income'][category.name] = []
        for specification in specifications:
            category_data['income'][category.name].append(specification.name)
    elif category.is_income == False:
        category_data['expense'][category.name] = []
        for specification in specifications:
            category_data['expense'][category.name].append(specification.name)
category_data = json.dumps(category_data)
'''
