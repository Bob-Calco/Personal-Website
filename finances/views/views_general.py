import finances.models as m
from django.db.models import Max, Sum
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from datetime import date
from finances.extend_timedelta import delta_months
from django.db import connection
import finances.database as db

@user_passes_test(lambda u: u.is_superuser)
def home(request):
    # get current total assets
    last_date = m.Balances.objects.aggregate(Max('date'))['date__max']
    assets = m.Balances.objects.filter(date=last_date).filter(item__asset=True).aggregate(Sum('amount'))['amount__sum']
    # get income statement of last three months
    this_month = date.today().replace(day=1)
    start_date = delta_months(this_month, -3)
    headers, data = db.income_statement(start_date, this_month)

    context = {
        'assets': assets,
        'data': data,
        'headers': headers,
    }
    return render(request, "finances/home.html", context)
