from django.shortcuts import render, redirect
from django.db import connection
import pj.forms as f
import pj.models as m

def signup(request):
    if request.method == "POST":
        form = f.AttendeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pj:view_turnout')
    else:
        form = f.AttendeeForm()
    context = {
        "form": form,
    }
    return render(request, "pj/signup.html", context)

def view_turnout(request):
    years = ['{}/{}'.format(r, r+1) for r in range(1966, 2017)]
    data = []
    with connection.cursor() as cursor:
        for year in years:
            query = "SELECT role, COUNT(*) FROM pj_attendee WHERE start_date <= '{}' and (end_date is null or end_date >= '{}') GROUP BY role".format(year, year)
            cursor.execute(query)
            result = cursor.fetchall()
            d = [year,0 ,0, 0]
            if len(result) > 0:
                ov = 0
                for row in result:
                    if row[0] == 'ST':
                        d[1] = row[1]
                    elif tup[0] == 'TE':
                        d[2] = row[1]
                    else:
                        ov += row[1]
                d[3] = ov
            data.append(d)
    context = {
        'data': data,
    }
    return render(request, "pj/view_turnout.html", context)
