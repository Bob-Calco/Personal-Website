from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from datetime import date

import finances.database as db

### YEAR TABLE VIEWS ###

@user_passes_test(lambda u: u.is_superuser)
def year_table(request, year=date.today().year):
    context = db.simple_year_table(year)
    return render(request, "finances/year-table.html", context)
