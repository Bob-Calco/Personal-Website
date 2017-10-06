from datetime import date
import finances.models as m
from django.db.models import Sum
from django.db import connection


def next_month(input_date=date.today()):
    if input_date.month == 12:
        output_date = date(input_date.year+1,1,1)
    else:
        output_date = date(input_date.year, input_date.month+1,1)
    return output_date

def income_statement(start, end):
    query = ("select strftime('%m', t.date) as 'month', c.is_income, round(sum(t.amount), 2) "
                    "from finances_transactions t "
                         "join finances_categories c "
                             "on t.category_id = c.id "
                    "where t.date >= '"+start.strftime('%Y-%m-%d')+"' and t.date < '"+end.strftime('%Y-%m-%d')+"' "
                    "group by strftime('%m', t.date), c.is_income "
                    "order by month, is_income")
    with connection.cursor() as cursor:
        cursor.execute(query)
        raw_data = cursor.fetchall()

    headers, data = [''], [['Expense'],['Income']]
    # put the distinct months in the first row
    for row in raw_data:
        if row[0] not in headers:
            headers.append(row[0])
    # add expenses to the second row and income to the third row
    for row in raw_data:
        if row[1] == False:
            i = headers.index(row[0])
            while i > len(data[0]):
                data[1].append('')
            data[0].append(row[2])
        else:
            i = headers.index(row[0])
            while i > len(data[1]):
                data[2].append('')
            data[1].append(row[2])
    # turn the month numbers to names
    for i, month in enumerate(headers[1:]):
        headers[i+1] = date(2000, int(month), 1).strftime('%B')
    return headers, data

def transactions(year=date.today().year, month=date.today().month):
    year = int(year)
    month = int(month)
    start = date(year, month, 1)
    end = next_month(start)
    transactions = m.Transactions.objects.filter(date__gte=start).filter(date__lt=end).order_by('date')
    return transactions

def categories():
    category_data = {}
    categories = m.Categories.objects.filter(specification_of__isnull=True)
    for category in categories:
        specifications = m.Categories.objects.filter(specification_of__isnull=False).filter(specification_of=category)
        category_data[category.name] = []
        for specification in specifications:
            category_data[category.name].append(specification.name)
    return category_data

def balance(year):
    year = int(year)

    # prepare data, we will append all values of a month to that list, this makes it easy to use in the template
    data = [['Jan'],['Feb'],['Mar'],['Apr'],['May'],['Jun'],['Jul'],['Aug'],['Sep'],['Okt'],['Nov'],['Dec']]

    # get the distinct balance items that were used during this year (returns list of pks)
    a_items = m.Balances.objects.filter(date__gte=date(year, 1, 1)).filter(date__lt=date(year+1, 1, 1)).filter(item__asset=True).values('item').distinct()
    l_items = m.Balances.objects.filter(date__gte=date(year, 1, 1)).filter(date__lt=date(year+1, 1, 1)).filter(item__asset=False).values('item').distinct()

    # turn list of pks to list of names to use in the template
    # the False and True variables are used in the template to determine whether it is a total column or not
    items = [['Total', False]]
    for item in a_items:
        items.append([m.BalanceItems.objects.get(id=item['item']).name, True])
    items.append(['Total', False])
    for item in l_items:
        items.append([m.BalanceItems.objects.get(id=item['item']).name, True])

    # append asset totals to each month (then append empty strings to empty months)
    a_totals = m.Balances.objects.filter(date__gte=date(year, 1, 1)).filter(date__lt=date(year+1, 1, 1)).filter(item__asset=True).values('date').annotate(Sum('amount')).order_by('date')
    for a in a_totals:
        mo = a['date'].month - 1
        data[mo].append(a['amount__sum'])
    for m_list in data:
        if len(m_list) == 1:
            m_list.append('')

    # append total per asset item to every month
    for item in a_items:
        for n in range(1,13):
            # .first() because there should only be one
            amount = m.Balances.objects.filter(item=m.BalanceItems.objects.get(id=item['item'])).filter(date=date(year, n, 1)).first()
            if amount is not None:
                data[n-1].append(amount.amount)
            else:
                data[n-1].append("")

    # append liabilities totals to each month (then append empty strings to empty months)
    l_totals = m.Balances.objects.filter(date__gte=date(year, 1, 1)).filter(date__lt=date(year+1, 1, 1)).filter(item__asset=False).values('date').annotate(Sum('amount')).order_by('date')
    for l in l_totals:
        mo = l['date'].month - 1
        data[mo].append(l['amount__sum'])
    for m_list in data:
        if len(m_list) == 2+len(a_items):
            m_list.append('')

    # append total per liability item to every month
    for item in l_items:
        for n in range(1,13):
            amount = m.Balances.objects.filter(item=m.BalanceItems.objects.get(id=item['item'])).filter(date=date(year, n, 1)).first()
            if amount is not None:
                data[n-1].append(amount.amount)
            else:
                data[n-1].append("")

    return (items, data, len(a_items), len(l_items))

def simple_year_table(year=date.today().year):
    # queries as to improve performance
    # query_sum_by_category_by_month = (
    #     "select strftime('%m', t.date) as 'month', c.name, c.id, round(sum(amount), 2) "
    #     "from finances_transactions t "
    #         "join finances_categories c "
    #             "on t.category_id = c.id "
    #     "where t.date >= '"+start.strftime('%Y-%m-%d')+"' and t.date < '"+end.strftime('%Y-%m-%d')+"' "
    #     "group by strftime('%m', t.date), c.id "
    #     "order by month, name"
    # )

    year = int(year)
    income = {}
    expense = {}

    # Get all the categories that we had in this year
    categories = m.Transactions.objects.filter(date__gte=date(year, 1, 1)).filter(date__lt=date(year+1, 1, 1)).values('category').distinct()

    # For every category get the data
    for category in categories:
        category = m.Categories.objects.get(pk=category['category'])
        l = [0,0,0,0,0,0,0,0,0,0,0,0,0]
        for i in range(0, 12):
            if i == 11:
                next_date = date(year+1, 1, 1)
            else:
                next_date = date(year, i+2, 1)
            s = m.Transactions.objects.filter(date__gte=date(year, i+1, 1)).filter(date__lt=next_date).filter(category=category).aggregate(Sum('amount'))['amount__sum']
            if s is not None:
                l[i] = s
        l[12] = m.Transactions.objects.filter(date__gte=date(year, 1, 1)).filter(date__lt=date(year+1, 1, 10)).filter(category=category).aggregate(Sum('amount'))['amount__sum']
        if category.is_income:
            income[category] = l
        else:
            expense[category] = l

    # Calculate the totals row
    income_totals = [0,0,0,0,0,0,0,0,0,0,0,0,0]
    expense_totals = [0,0,0,0,0,0,0,0,0,0,0,0,0]
    for i in range(1,13):
        if i == 12:
            next_date = date(year+1, 1, 1)
        else:
            next_date = date(year, i+1, 1)
        it = m.Transactions.objects.filter(date__gte=date(year, i, 1)).filter(date__lt=next_date).filter(category__is_income=True).aggregate(Sum('amount'))['amount__sum']
        et = m.Transactions.objects.filter(date__gte=date(year, i, 1)).filter(date__lt=next_date).filter(category__is_income=False).aggregate(Sum('amount'))['amount__sum']
        if it is not None:
            income_totals[i-1] = it
        if et is not None:
            expense_totals[i-1] = et
    it = m.Transactions.objects.filter(date__gte=date(year, 1, 1)).filter(date__lt=date(year+1, 1, 1)).filter(category__is_income=True).aggregate(Sum('amount'))['amount__sum']
    et = m.Transactions.objects.filter(date__gte=date(year, 1, 1)).filter(date__lt=date(year+1, 1, 1)).filter(category__is_income=False).aggregate(Sum('amount'))['amount__sum']
    if it is not None:
        income_totals[12] = it
    if et is not None:
        expense_totals[12] = et

    errors = [0,0,0,0,0,0,0,0,0,0,0,0]
    for i in range(1,13):
        transactions_change = (income_totals[i-1] - expense_totals[i-1])

        if i == 1:
            prev_month = date(year-1, 12, 1)
            this_month = date(year, 1, 1)
        else:
            prev_month = date(year, i-1, 1)
            this_month = date(year, i, 1)

        assets_1 = m.Balances.objects.filter(date=prev_month).filter(item__asset=True).aggregate(Sum('amount'))['amount__sum']
        liabilities_1 = m.Balances.objects.filter(date=prev_month).filter(item__asset=False).aggregate(Sum('amount'))['amount__sum']
        assets_2 = m.Balances.objects.filter(date=this_month).filter(item__asset=True).aggregate(Sum('amount'))['amount__sum']
        liabilities_2 = m.Balances.objects.filter(date=this_month).filter(item__asset=False).aggregate(Sum('amount'))['amount__sum']
        try:
            balance_change = (assets_2 - liabilities_2) - (assets_1 - liabilities_1)
        except TypeError:
            balance_change = transactions_change

        errors[i-1] = balance_change - transactions_change

    errors.append(sum(errors))

    context = {
        'income': income,
        'expense': expense,
        'income_totals': income_totals,
        'expense_totals': expense_totals,
        'errors': errors,
    }

    return context
