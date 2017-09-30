from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.contrib import messages
import pj.forms as f
import pj.models as m
import csv

def signup(request):
    if request.method == "POST":
        form = f.AttendeeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Je bent aangemeld!')
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
                    elif row[0] == 'TE':
                        d[2] = row[1]
                    else:
                        ov += row[1]
                d[3] = ov
            data.append(d)
    total_signups = m.Attendee.objects.count()
    context = {
        'data': data,
        'total_signups': total_signups
    }
    return render(request, "pj/view_turnout.html", context)

@login_required
def export_attendees(request):
    attendees = m.Attendee.objects.all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="pjubeljaar_aanmeldingen.csv"'

    writer = csv.writer(response, delimiter=';')
    writer.writerow(['Voornaam', 'Achternaam', 'Meisjesnaam', 'Geboortedatum', 'Email', 'Rol', 'Startdatum', 'Einddatum', 'Laatste klas', 'Klas veranderd', 'Jaar veranderd', 'Aanmelddatum'])
    for a in attendees:
        writer.writerow([a.first_name, a.last_name, a.maiden_name, a.date_of_birth, a.email, a.role, a.start_date, a.end_date, a.last_class, a.class_change, a.class_change_year, a.created_timestamp])
    return response

@login_required
def list_of_attendees(request):
    attendees = m.Attendee.objects.all()
    context = {
        'total': len(attendees),
        'attendees': attendees,
    }
    return render(request, "pj/list_of_attendees.html", context)
