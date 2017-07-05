import json
import finances.models as m
import finances.forms as f
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from django.core import serializers
from django.db import connection
from django.db.models import Sum
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
            return redirect('finances:default_transactions')
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
    # will go wrong if an item is missing for a month, which means always except if the whole year is filled up...
    year = int(year)
    data = [['Jan'],['Feb'],['Mar'],['Apr'],['May'],['Jun'],['Jul'],['Aug'],['Sep'],['Okt'],['Nov'],['Dec']]
    a_items = m.Balances.objects.filter(date__gte=date(year, 1, 1)).filter(date__lt=date(year+1, 1, 1)).filter(item__asset=True).values('item').distinct()
    l_items = m.Balances.objects.filter(date__gte=date(year, 1, 1)).filter(date__lt=date(year+1, 1, 1)).filter(item__asset=False).values('item').distinct()

    a_totals = m.Balances.objects.filter(date__gte=date(year, 1, 1)).filter(date__lt=date(year+1, 1, 1)).filter(item__asset=True).values('date').annotate(Sum('amount')).order_by('date')
    for a in a_totals:
        mo = a['date'].month - 1
        data[mo].append(a['amount__sum'])
    for item in a_items:
        for n in range(1,13):
            amount = m.Balances.objects.filter(item=m.BalanceItems.objects.get(id=item['item'])).filter(date=date(year, n, 1)).first()
            if amount is not None:
                data[n-1].append(amount.amount)
            else:
                data[n-1].append("")

    l_totals = m.Balances.objects.filter(date__gte=date(year, 1, 1)).filter(date__lt=date(year+1, 1, 1)).filter(item__asset=False).values('date').annotate(Sum('amount')).order_by('date')
    for l in l_totals:
        mo = l['date'].month - 1
        data[mo].append(l['amount__sum'])
    for item in l_items:
        for n in range(1,13):
            amount = m.Balances.objects.filter(item=m.BalanceItems.objects.get(id=item['item'])).filter(date=date(year, n, 1)).first()
            if amount is not None:
                data[n-1].append(amount.amount)
            else:
                data[n-1].append("")

    context = {
        'data': data,
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
        print(forms.errors)
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
    context = None
    return render(request, "finances/home.html", context)

### YEAR TABLE VIEWS ###

@user_passes_test(lambda u: u.is_superuser)
def year_table(request, year=date.today().year):
    year = int(year)
    income = {}
    expense = {}

    # Get all the categories that we had in this year
    categories = m.Transactions.objects.filter(date__gte=date(year, 1, 1)).filter(date__lt=date(year+1, 1, 1)).values('category').distinct()

    # For every category get the data
    for category in categories:
        category = m.Categories.objects.get(pk=category['category'])
        l = [0,0,0,0,0,0,0,0,0,0,0,0,0]
        for i in range(0, 12):
            if i == 11:
                next_date = date(year+1, 1, 1)
            else:
                next_date = date(year, i+2, 1)
            s = m.Transactions.objects.filter(date__gte=date(year, i+1, 1)).filter(date__lt=next_date).filter(category=category).aggregate(Sum('amount'))['amount__sum']
            if s is not None:
                l[i] = s
        l[12] = m.Transactions.objects.filter(date__gte=date(year, 1, 1)).filter(date__lt=date(year+1, 1, 10)).filter(category=category).aggregate(Sum('amount'))['amount__sum']
        if category.is_income:
            income[category] = l
        else:
            expense[category] = l

    # Calculate the totals row
    income_totals = [0,0,0,0,0,0,0,0,0,0,0,0,0]
    expense_totals = [0,0,0,0,0,0,0,0,0,0,0,0,0]
    for i in range(1,13):
        if i == 12:
            next_date = date(year+1, 1, 1)
        else:
            next_date = date(year, i+1, 1)
        it = m.Transactions.objects.filter(date__gte=date(year, i, 1)).filter(date__lt=next_date).filter(category__is_income=True).aggregate(Sum('amount'))['amount__sum']
        et = m.Transactions.objects.filter(date__gte=date(year, i, 1)).filter(date__lt=next_date).filter(category__is_income=False).aggregate(Sum('amount'))['amount__sum']
        if it is not None:
            income_totals[i-1] = it
        if et is not None:
            expense_totals[i-1] = et
    it = m.Transactions.objects.filter(date__gte=date(year, 1, 1)).filter(date__lt=date(year+1, 1, 1)).filter(category__is_income=True).aggregate(Sum('amount'))['amount__sum']
    et = m.Transactions.objects.filter(date__gte=date(year, 1, 1)).filter(date__lt=date(year+1, 1, 1)).filter(category__is_income=False).aggregate(Sum('amount'))['amount__sum']
    if it is not None:
        income_totals[12] = it
    if et is not None:
        expense_totals[12] = et

    context = {
        'income': income,
        'expense': expense,
        'income_totals': income_totals,
        'expense_totals': expense_totals
    }
    return render(request, "finances/year-table.html", context)

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
