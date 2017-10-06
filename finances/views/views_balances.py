import finances.models as m
import finances.forms as f
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from datetime import date

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
