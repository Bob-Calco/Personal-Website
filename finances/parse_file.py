import csv
import re
import finances.models as m

def parse(f, dataset):
    # get relevant search terms
    search_fields = m.SearchTerms.objects.filter(dataset=dataset).values('field').distinct()
    searches = {}
    for field in search_fields:
        searches[field] = m.SearchTerms.objects.filter(dataset=dataset).filter(field=field)

    # open the file
    r = csv.reader(f)
    next(r, None)
    for row in r:
        for field in searches:
            for term in searches[field]:
                found = re.search(term.term, row[field])
                if found is not None:
                    ins = m.Transactions(date=row['Datum'], amount=row['Bedrag (EUR)'], category=, specification=,)
                    ins.save()
                    break
