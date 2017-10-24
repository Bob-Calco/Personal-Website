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

    totals_query = (
        "select asset.date, asset.a, round(sum, 2) "
        "from "
            "((select 0 as 'a' union select 1) join "
            "(select distinct date "
            "from finances_balances as b "
            "where date >= '{0}-01-01' and date < '{1}-01-01')) asset "
            "left join "
            "(select date, asset, sum(amount) as sum "
            "from finances_balances as b "
                "join finances_balanceitems as bi "
                    "on b.item_id = bi.id "
            "where date >= '{0}-01-01' and date < '{1}-01-01' "
            "group by date, asset) balance "
            "on asset.date = balance.date and asset.a = balance.asset "
        "order by asset.date, asset.a "
    )
    balance_query = (
        "select dates.date, items.name, items.asset, amounts.amount "
        "from "
            "(select distinct bi.name, bi.asset "
            "from finances_balances as b "
                "join finances_balanceitems as bi "
                    "on b.item_id = bi.id "
            "where date >= '{0}-01-01' and date < '{1}-01-01') items "
            "join "
            "(select distinct date "
            "from finances_balances "
            "where date >= '{0}-01-01' and date < '{1}-01-01') dates "
            "left join "
            "(select b.amount, bi.name, b.date "
            "from finances_balances as b "
                "join finances_balanceitems as bi "
                    "on b.item_id = bi.id "
            "where date >= '{0}-01-01' and date < '{1}-01-01') amounts "
        "on amounts.name = items.name and dates.date = amounts.date "
        "order by dates.date, items.asset desc, items.name "
    )
    with connection.cursor() as cursor:
        cursor.execute(totals_query.format(year, year+1))
        totals_raw_data = cursor.fetchall()
        cursor.execute(balance_query.format(year, year+1))
        balance_raw_data = cursor.fetchall()

    # the loose True and False variables say whether this item is a total or not

    # balance items in scope
    asset_count = 0
    liabilities_count = 0
    items = [['Total', True]]

    month = balance_raw_data[0][0]
    in_assets = True
    for row in balance_raw_data:
        if row[0] != month:
            break
        if in_assets:
            if row[2] == False:
                in_assets = False
                items.append(['Total', True])
        if in_assets:
            asset_count += 1
        else:
            liabilities_count += 1
        items.append([row[1], False])

    # first data column is the total of the assets that month
    for row in totals_raw_data:
        if row[1] == True:
            data[row[0].month-1].append([row[2], True])

    # next come all the different asset balance items
    for row in balance_raw_data:
        if row[2] == True:
            data[row[0].month-1].append([row[3], False])

    # then the total of the liabilities that month
    for row in totals_raw_data:
        if row[1] == False:
            data[row[0].month-1].append([row[2], True])

    # finally add all the different liabilities balance items
    for row in balance_raw_data:
        if row[2] == False:
            data[row[0].month-1].append([row[3], False])

    return (items, data, asset_count, liabilities_count)

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
