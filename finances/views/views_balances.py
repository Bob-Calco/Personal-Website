import finances.models as m
import finances.forms as f
from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.contrib.auth.decorators import user_passes_test
from datetime import date
from django.template.loader import render_to_string

import finances.database as db


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
    if request.method == 'POST':
        forms = f.BalanceFormSet(request.POST, queryset=m.Balances.objects.filter(date=date(int(year), int(month), 1)))
        if forms.is_valid():
            forms.save()
            return JsonResponse({'saved': True})
    else:
        forms = f.BalanceFormSet(queryset=m.Balances.objects.filter(date=date(int(year), int(month), 1)))
    context = {
        'forms': forms,
        'year': year,
        'month': date(1900, int(month), 1).strftime('%B'),
        'monthnumber': month
    }
    html = render_to_string("finances/balance-edit.html", context, request=request)
    return JsonResponse({'saved': False, 'html': html})
