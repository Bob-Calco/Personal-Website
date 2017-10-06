import finances.models as m
import finances.forms as f
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from datetime import date

@user_passes_test(lambda u: u.is_superuser)
def balance_items(request):
    data = m.BalanceItems.objects.all()
    return render(request, 'finances/balance-items.html', {'data': data})

@user_passes_test(lambda u: u.is_superuser)
def upsert_balance_item(request, pk=None):
    if request.method == 'POST':
        if pk is None:
            form = f.BalanceItemForm(request.POST)
            add = True
        else:
            form = f.BalanceItemForm(request.POST, instance=m.BalanceItems.objects.get(id=pk))
            add = False
        if form.is_valid():
            form.save()
            return redirect('finances:balance_items')
    else:
        if pk is None:
            form = f.BalanceItemForm()
            add = True
        else:
            form = f.BalanceItemForm(instance=m.BalanceItems.objects.get(id=pk))
            add = False
    context = {
        'form': form,
        'add': add,
    }
    return render(request, 'finances/balance-item.html', context)

@user_passes_test(lambda u: u.is_superuser)
def delete_balance_item(request, pk):
    m.BalanceItems.objects.get(id=pk).delete()
    return redirect('finances:balance_items')
