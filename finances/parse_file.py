import csv
import re
import finances.models as m
from datetime import datetime

def parse(f, dataset):
    # get relevant search terms
    search_fields = m.SearchTerms.objects.filter(dataset=dataset).values('field').distinct()
    searches = {}
    for field in search_fields:
        searches[field['field']] = m.SearchTerms.objects.filter(dataset=dataset).filter(field=field['field'])

    # open the file
    print(searches)
    r = csv.DictReader(f)
    for row in r:
        for field in searches:
            check = False
            for term in searches[field]:
                found = re.search(term.term, row[field])
                if found is not None:
                    ins = m.Transactions(date=datetime.strptime(row['Datum'], '%Y%m%d').date(), amount=row['Bedrag (EUR)'].replace(',', '.'), category=term.category, specification=term.specification)
                    ins.save()
                    check = True
                    break
            if check == True:
                break
        m.UnprocessedTransactions(payload=str(row), dataset=dataset).save()
