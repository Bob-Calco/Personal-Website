from django.shortcuts import render
import scrum.models as m
import scrum.forms as f

def product_backlog(request):
    userstories = m.Userstories.objects.all()
    epics = m.Epics.objects.all()
    us_epic = {}
    for epic in epics:
        us_epic[epic] = m.Userstories.objects.filter(epic__id=epic.id)
    us_form = f.UserstoriesForm(prefix="us")
    epic_form = f.EpicForm(prefix="epic")

    context = {
        "title": "Product Backlog",
        "userstories": userstories,
        "us_epic": us_epic,
        "us_form": us_form,
        "epic_form": epic_form,
        }
    return render(request, "scrum/product_backlog.html", context)

def add_userstory(request):
    if request.method == "POST":
        form = f.UserstoriesForm(request.POST)
        if form.is_valid():
            form.save()

def add_epic(request):
    if request.method == "POST":
        form = f.EpicForm(request.POST)
        if form.is_valid():
            form.save()
