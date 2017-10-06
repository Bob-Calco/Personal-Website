import json
import finances.models as m
import finances.forms as f
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse
from datetime import date
from io import TextIOWrapper
import ast

import finances.database as db
import finances.parse_file as parse_file

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
