import json
import finances.models as m
import finances.forms as f
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from django.core import serializers

@user_passes_test(lambda u: u.is_superuser)
def home(request):
    context = None
    return render(request, "finances/home.html", context)

@user_passes_test(lambda u: u.is_superuser)
def transactions(request):
    if request.method =="GET":
        transactions = m.Transactions.objects.order_by('date')
        context = {
            "transactions": transactions,
        }
        return render(request, "finances/transactions.html", context)

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
def categories(request):
    context = None
    return render(request, "finances/home.html", context)

@user_passes_test(lambda u: u.is_superuser)
def balance(request):
    context = None
    return render(request, "finances/home.html", context)

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
