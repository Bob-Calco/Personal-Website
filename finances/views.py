import json
import finances.models as m
import finances.forms as f
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.db import connection
from django.db.models import Sum
from datetime import date
from io import TextIOWrapper
import ast

import finances.database as db
import finances.parse_file as parse_file

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
        transactions = db.transactions(year, month)
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
            return redirect('finances:default_transactions')
        else:
            errors = True

    category_data = json.dumps(db.categories())

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
    return redirect('finances:default_transactions')

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
    items, data, a_len, l_len = db.balance(year)
    context = {
        'data': data,
        'a_len': a_len+1,
        'l_len': l_len+1,
        'items': items,
        'year': year
    }
    return render(request, "finances/balance.html", context)

@user_passes_test(lambda u: u.is_superuser)
def balance_edit(request, year, month):
    errors = False
    if request.method == 'POST':
        forms = f.BalanceFormSet(request.POST, queryset=m.Balances.objects.filter(date=date(int(year), int(month), 1)))
        if forms.is_valid():
            forms.save()
            return redirect('finances:balance', year=year)
        else:
            errors = True
    if errors == True:
        pass
    else:
        forms = f.BalanceFormSet(queryset=m.Balances.objects.filter(date=date(int(year), int(month), 1)))
    context = {
        'forms': forms,
        'year': year,
        'month': date(1900, int(month), 1).strftime('%B'),
        'monthnumber': month
    }
    return render(request, 'finances/balance-edit.html', context)

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

### YEAR TABLE VIEWS ###

@user_passes_test(lambda u: u.is_superuser)
def year_table(request, year=date.today().year):
    context = db.simple_year_table(year)
    return render(request, "finances/year-table.html", context)

### PROCESS UPLOADED FILE ###

@user_passes_test(lambda u:u.is_superuser)
def upload_file(request):
    if request.method == 'POST':
        form = f.UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = TextIOWrapper(request.FILES['file'].file, encoding='utf-8', errors='replace')
            parse_file.parse(file, form.cleaned_data['dataset'])
            return redirect('finances:home')
    else:
        form = f.UploadFileForm()
    return render(request, 'finances/upload-file.html', {'form': form})

@user_passes_test(lambda u:u.is_superuser)
def process_unprocessed_transactions(request):
    datasets = m.UnprocessedTransactions.objects.values('dataset').distinct()
    data = []
    for dataset in datasets:
        dataset = dataset['dataset']
        raw_data = m.UnprocessedTransactions.objects.filter(dataset=dataset)
        da = []
        for d in raw_data:
            da.append({'id': d.id, 'payload': ast.literal_eval(d.payload)})
        data.append(da)
    form = f.TransactionForm()

    category_data = json.dumps(db.categories())

    context = {
        'data': data,
        'form': form,
        'category_data': category_data
    }

    return render(request, 'finances/unprocessed-transactions.html', context)

@user_passes_test(lambda u:u.is_superuser)
def delete_unprocessed_transaction(request, pk):
    m.UnprocessedTransactions.objects.get(id=pk).delete()
    data = {
        'deleted': True
    }
    return JsonResponse(data)

@user_passes_test(lambda u:u.is_superuser)
def process_transaction(request):
    if request.method == "POST":
        form = f.TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'saved': True})
        else:
            return JsonResponse({'saved': False})
