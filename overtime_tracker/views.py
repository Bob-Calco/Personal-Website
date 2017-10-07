from django.shortcuts import render, redirect
from django.db.models import Sum
import overtime_tracker.forms as f
import overtime_tracker.models as m
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.urlresolvers import reverse
from overtime_tracker.outlook_functions import get_signin_url, get_me, get_token_from_code, get_access_token, get_my_events
import time
import overtime_tracker.get_data as gd
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import date
import json

@user_passes_test(lambda u: u.is_superuser)
def home(request):
    year = date.today().year

    current_overtime = round(m.Day.objects.all().aggregate(Sum('hours_overtime'))['hours_overtime__sum'], 2)
    vacation_used = m.Day.objects.filter(date__gte=date(year, 1, 1)).filter(date__lt=date(year+1, 1, 1)).aggregate(Sum('hours_vacation'))['hours_vacation__sum']
    vacation_left = round(m.VacationHours.objects.get(year=date(year, 1, 1)).amount - vacation_used, 2)

    total_worktime = round(m.Day.objects.all().aggregate(Sum('hours_worked'))['hours_worked__sum'], 2)
    total_standby = round(m.Day.objects.all().aggregate(Sum('hours_standby'))['hours_standby__sum'], 2)
    total_vacation = round(m.Day.objects.all().aggregate(Sum('hours_vacation'))['hours_vacation__sum'], 2)
    total_holidays = round(m.Day.objects.filter(holiday=True).count(), 2)

    days = m.Day.objects.all().order_by('date')
    running_overtime = []
    running_total = 0
    for day in days:
        running_total = round(running_total + day.hours_overtime, 2)
        running_overtime.append(running_total)
    labels = json.dumps([i for i in range(0, len(days))])
    data = json.dumps(running_overtime)

    context = {
        'sign_in_url': outlook_signin(request),
        'total_worktime': total_worktime,
        'total_standby': total_standby,
        'total_vacation': total_vacation,
        'total_holidays': total_holidays,
        'current_overtime': current_overtime,
        'vacation_left': vacation_left,
        'year': year,
        'data': data,
        'labels': labels,
    }
    return render(request, 'overtime_tracker/home.html', context)

### OUTLOOK AUTH VIEWS ###

@user_passes_test(lambda u: u.is_superuser)
def outlook_signin(request):
    redirect_uri = request.build_absolute_uri(reverse('overtime_tracker:gettoken'))
    sign_in_url = get_signin_url(redirect_uri)
    return sign_in_url

@user_passes_test(lambda u: u.is_superuser)
def gettoken(request):
    auth_code = request.GET['code']
    redirect_uri = request.build_absolute_uri(reverse('overtime_tracker:gettoken'))
    token = get_token_from_code(auth_code, redirect_uri)
    access_token = token['access_token']
    user = get_me(access_token)
    refresh_token = token['refresh_token']
    expires_in = token['expires_in']

    # expires_in is in seconds
    # Get current timestamp (seconds since Unix Epoch) and
    # add expires_in to get expiration time
    # Subtract 5 minutes to allow for clock differences
    expiration = int(time.time()) + expires_in - 300

    # Save the token in the session
    request.session['access_token'] = access_token
    request.session['refresh_token'] = refresh_token
    request.session['token_expires'] = expiration
    request.session['user_email'] = user['userPrincipalName']
    return HttpResponseRedirect(reverse('overtime_tracker:wait_for_processing'))

@user_passes_test(lambda u: u.is_superuser)
def wait_for_processing(request):
    context = {
        'sign_in_url': outlook_signin(request),
    }
    return render(request, 'overtime_tracker/wait.html', context)

@user_passes_test(lambda u: u.is_superuser)
def process_data(request):
    access_token = get_access_token(request, request.build_absolute_uri(reverse('overtime_tracker:gettoken')))
    user_email = request.session['user_email']
    # If there is no token in the session, redirect to home
    if not access_token:
        return HttpResponseRedirect(reverse('overtime_tracker:outlook_signin'))
    else:
        dates, start_date, end_date = gd.get_dates_to_process()
        outlook_events = get_my_events(access_token, user_email, start_date, end_date)['value']
        toggl_data = gd.get_toggl_data(start_date, end_date)
        gd.process_data(dates, toggl_data, outlook_events)
        url = request.build_absolute_uri(reverse('overtime_tracker:read_days'))
        return JsonResponse({'url': url})

### DAY VIEWS ###

@user_passes_test(lambda u: u.is_superuser)
def read_days(request):
    days_list = m.Day.objects.all().order_by('-date')
    paginator = Paginator(days_list, 20)
    page = request.GET.get('page')
    try:
        days = paginator.page(page)
    except PageNotAnInteger:
        days = paginator.page(1)
    except EmptyPage:
        days = paginator.page(paginator.num_pages)
    context = {
        'days': days,
        'sign_in_url': outlook_signin(request),
    }
    return render(request, 'overtime_tracker/days.html', context)

@user_passes_test(lambda u: u.is_superuser)
def upsert_day(request, pk=None):
    if request.method == "POST":
        if pk is not None:
            form = f.DayForm(request.POST, instance=m.Day.objects.get(id=pk))
        else:
            form = f.DayForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('overtime_tracker:read_days')
    else:
        if pk is not None:
            form =f.DayForm(instance=m.Day.objects.get(id=pk))
        else:
            form = f.DayForm()
    context = {
        'form': form,
        'add': True if pk is None else False,
        'sign_in_url': outlook_signin(request),
    }
    return render(request, 'overtime_tracker/day.html', context)

@user_passes_test(lambda u: u.is_superuser)
def delete_day(request, pk):
    m.Day.objects.get(id=pk).delete()
    return redirect('overtime_tracker:read_days')

### CONFIGURATION VIEWS ###

@user_passes_test(lambda u: u.is_superuser)
def read_configs(request):
    configs = m.Configuration.objects.all()
    context = {
        'configs': configs,
        'sign_in_url': outlook_signin(request),
    }
    return render(request, 'overtime_tracker/configs.html', context)

@user_passes_test(lambda u: u.is_superuser)
def upsert_config(request, pk=None):
    if request.method == "POST":
        if pk is not None:
            form = f.ConfigurationForm(request.POST, instance=m.Configuration.objects.get(id=pk))
        else:
            form = f.ConfigurationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('overtime_tracker:read_configs')
    else:
        if pk is not None:
            form =f.ConfigurationForm(instance=m.Configuration.objects.get(id=pk))
        else:
            form = f.ConfigurationForm()
    context = {
        'form': form,
        'add': True if pk is None else False,
        'sign_in_url': outlook_signin(request),
    }
    return render(request, 'overtime_tracker/config.html', context)

def delete_config(request, pk):
    m.Configuration.objects.get(id=pk).delete()
    return redirect('overtime_tracker:read_configs')

### VACATION HOURS VIEWS ###

@user_passes_test(lambda u: u.is_superuser)
def read_vacation_hours(request):
    vacation_hours = m.VacationHours.objects.all()
    context = {
        'vacation_hours': vacation_hours,
        'sign_in_url': outlook_signin(request),
    }
    return render(request, 'overtime_tracker/vacation_hours.html', context)

@user_passes_test(lambda u: u.is_superuser)
def upsert_vacation_hours(request, pk=None):
    if request.method == "POST":
        if pk is not None:
            form = f.VacationHoursForm(request.POST, instance=m.VacationHours.objects.get(id=pk))
        else:
            form = f.VacationHoursForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('overtime_tracker:read_vacation_hours')
    else:
        if pk is not None:
            form =f.VacationHoursForm(instance=m.VacationHours.objects.get(id=pk))
        else:
            form = f.VacationHoursForm()
    context = {
        'form': form,
        'add': True if pk is None else False,
        'sign_in_url': outlook_signin(request),
    }
    return render(request, 'overtime_tracker/vacation_hour.html', context)

@user_passes_test(lambda u: u.is_superuser)
def delete_vacation_hours(request, pk):
    m.VacationHours.objects.get(id=pk).delete()
    return redirect('overtime_tracker:read_vacation_hours')
