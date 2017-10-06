import json
import finances.models as m
import finances.forms as f
from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.contrib.auth.decorators import user_passes_test
from datetime import date
from django.template.loader import render_to_string

import finances.database as db

### TRANSACTION VIEWS ###

@user_passes_test(lambda u: u.is_superuser)
def transactions(request, year=date.today().year, month=date.today().month):
    year = int(year)
    month = int(month)
    if request.method =="GET":
        transactions = db.transactions(year, month)
        category_data = json.dumps(db.categories())
        context = {
            "transactions": transactions,
            "year": year,
            "month": month,
            'category_data': category_data
        }
        return render(request, "finances/transactions.html", context)

@user_passes_test(lambda u: u.is_superuser)
def transaction(request, number=None):
    if request.method == "POST":
        if number is not None:
            transaction = m.Transactions.objects.get(id=number)
            form = f.TransactionForm(request.POST, instance=transaction)
            add = False
        else:
            form = f.TransactionForm(request.POST)
            add = True
        if form.is_valid():
            transaction = form.save()
            t_id = transaction.id
            html = render_to_string("finances/transaction-row.html", {'transaction': transaction})
            return JsonResponse({'saved': True, 'add': add, 'html': html, 't_id': t_id})

    else:
        if number is not None:
            transaction = m.Transactions.objects.get(id=number)
            form = f.TransactionForm(instance=transaction)
            add = False
        else:
            form = f.TransactionForm()
            add = True
    context = {
        "form": form,
        "add": add,
    }
    html = render_to_string("finances/transaction.html", context, request=request)
    return JsonResponse({'saved': False, 'add': add, 'html': html})

@user_passes_test(lambda u: u.is_superuser)
def delete_transaction(request, number):
    m.Transactions.objects.get(id=number).delete()
    return redirect('finances:default_transactions')
