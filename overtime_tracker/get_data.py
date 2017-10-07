import base64
from requests.auth import HTTPBasicAuth
import requests
import json
from datetime import datetime, timedelta, date
import overtime_tracker.models as m
from django.db.models import Max
from django.conf import settings

def get_dates_to_process():
    # find which dates to process
    last_date = m.Day.objects.aggregate(Max('date'))['date__max']
    start_date = last_date + timedelta(days=1)
    end_date = date.today()
    delta = end_date - start_date
    dates = {}
    for i in range(delta.days):
        dates[start_date + timedelta(days=i)] = m.Day(date=start_date + timedelta(days=i))
    return dates, start_date, end_date

def get_toggl_data(start_date, end_date):
    # Get hours_worked from Toggl
    # project_url = 'https://www.toggl.com/api/v8/projects/37721088'
    time_entries_url = 'https://www.toggl.com/api/v8/time_entries?start_date={start_date}T00%3A00%3A00%2B00%3A00&end_date={end_date}T00%3A00%3A00%2B00%3A00'
    url = time_entries_url.format(start_date=start_date.strftime('%Y-%m-%d'), end_date=end_date.strftime('%Y-%m-%d'))
    r = requests.get(url, auth=HTTPBasicAuth(settings.TOGGL_API_TOKEN, 'api_token'))
    data = json.loads(r.text)
    return data

def process_data(dates, toggl_data, outlook_events):
    # get holidays
    for a in dates:
        if is_holiday(a):
            dates[a].holiday = True

    for entry in toggl_data:
        try:
            if entry['pid'] == 37721088:
                d = datetime.strptime(entry['start'], '%Y-%m-%dT%H:%M:%S+00:00').date()
                duration = entry['duration']/3600
                dates[d].hours_worked += duration
        except KeyError:
            pass

    # get vacation and standby hours from Outlook
    # don't count saturday and sunday as vacation hours
    for event in outlook_events:
        if 'standby' in event['subject'].lower():
            start_date = datetime.strptime(event['start']['dateTime'], '%Y-%m-%dT%H:%M:%S.0000000').date()
            end_date = datetime.strptime(event['end']['dateTime'], '%Y-%m-%dT%H:%M:%S.0000000').date()
            delta = end_date - start_date
            for i in range(delta.days):
                if start_date + timedelta(days=i) in dates:
                    dates[start_date + timedelta(days=i)].hours_standby = 24 - dates[start_date + timedelta(days=i)].hours_worked

        if 'vakantie' in event['subject'].lower():
            start_date = datetime.strptime(event['start']['dateTime'], '%Y-%m-%dT%H:%M:%S.0000000').date()
            end_date = datetime.strptime(event['end']['dateTime'], '%Y-%m-%dT%H:%M:%S.0000000').date()
            delta = end_date - start_date
            for i in range(delta.days):
                if start_date + timedelta(days=i) in dates:
                    if (start_date + timedelta(days=i)).weekday() not in [5, 6]:
                        dates[start_date + timedelta(days=i)].hours_vacation = 8

    # save all the dates
    for key, model in dates.items():
        model.save()

def is_holiday(d):
    easter = calc_easter(d.year)
    if d.day == 1 and d.month == 1:
        return True # Nieuwjaar
    elif d == (easter - timedelta(days=2)):
        return True # goede vrijdag
    elif d == easter:
        return True # pasen
    elif d == (easter + timedelta(days=1)):
        return True # 2de paasdag
    elif d.month == 4 and d.day == 26 and d.weekday() == 5:
        return True # koningsdag (als 27 zondag is)
    elif d.month == 4 and d.day == 27 and d.weekday() != 6:
        return True # koningsdag
    elif d.month == 5 and d.day == 5 and (d.year % 5 == 0):
        return True # bevrijdingsdag
    elif d == (easter + timedelta(days=39)):
        return True # hemelvaart
    elif d == (easter + timedelta(days=49)):
        return True # pinksteren
    elif d == (easter + timedelta(days=50)):
        return True # 2de pinksterdag
    elif d.month == 12 and d.day == 25:
        return True # kerst
    elif d.month == 12 and d.day == 26:
        return True # 2de kerstdag
    else:
        return False

def calc_easter(year):
    "Returns Easter as a date object."
    a = year % 19
    b = year // 100 # amount of centuries
    c = year % 100 # remove centuries
    d = (19 * a + b - b // 4 - ((b - (b + 8) // 25 + 1) // 3) + 15) % 30
    e = (32 + 2 * (b % 4) + 2 * (c // 4) - d - (c % 4)) % 7
    f = d + e - 7 * ((a + 11 * d + 22 * e) // 451) + 114
    month = f // 31
    day = f % 31 + 1
    return date(year, month, day)
