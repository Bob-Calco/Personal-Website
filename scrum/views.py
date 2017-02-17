from django.shortcuts import render
import scrum.models as m

def product_backlog(request):
    userstories = m.Userstories.objects.all()
    epics = m.Epics.objects.all()
    us_epic = {}
    for epic in epics:
        us_epic[epic] = m.Userstories.objects.filter(epic__id=epic.id)
    context = {
        "title": "Product Backlog",
        "userstories": userstories,
        "us_epic": us_epic,
        }
    return render(request, "scrum/product_backlog.html", context)
