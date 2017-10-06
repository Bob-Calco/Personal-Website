from datetime import date
def delta_months(d, m):
    if m > 0:
        if d.month + m > 12:
            return date(d.year+1, d.month+m-12, d.day)
        else:
            return date(d.year, d.month+m, d.day)
    if m < 0:
        if d.month + m < 1:
            return date(d.year-1, d.month+m+12, d.day)
        else:
            return date(d.year, d.month+m, d.day)
