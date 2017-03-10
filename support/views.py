from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.contrib.auth.models import User

import support.forms as f
import support.models as m

@login_required
def inbox(request):
    if request.method == "POST":
        form = f.SupportMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.user = request.user
            message.save()
            data = serializers.serialize("json", [message,])
            return HttpResponse(data, content_type='application/json')
        else:
            return redirect('groceries:home')
    else:
        form = f.SupportMessageForm()
        messages = m.SupportMessages.objects.filter(user=request.user)
        messages.filter(reply=True).update(delivered=True)
        context = {
            "messages": messages,
            "form": form
        }
        return render(request, "support/inbox.html", context)

@login_required
def user_overview(request):
    if not request.user.is_superuser:
        return redirect('support:inbox')
    else:
        user_objects = User.objects.filter(is_superuser=False)
        users = []
        for user in user_objects:
            users.append( (user, m.SupportMessages.objects.filter(user=user).filter(reply=False).filter(delivered=False).count()) )
        context = {
            "users": users,
        }
        return render(request, "support/user-overview.html", context)

@login_required
def user(request, id):
    if not request.user.is_superuser:
        return redirect('support:inbox')
    else:
        if request.method == "POST":
            form = f.SupportMessageForm(request.POST)
            if form.is_valid():
                message = form.save(commit=False)
                message.user = User.objects.filter(id=id)[0]
                message.reply = True
                message.save()
                data = serializers.serialize("json", [message,])
                return HttpResponse(data, content_type='application/json')
            else:
                return redirect('support:user_overview')
        else:
            form = f.SupportMessageForm(request.POST)
            user = User.objects.filter(id=id)[0]
            messages = m.SupportMessages.objects.filter(user=user)
            messages.filter(reply=False).filter(delivered=False).update(delivered=True)
            context = {
                "user": user,
                "messages": messages,
                "form": form,
            }
            return render(request, "support/inbox.html", context)

@login_required
def check_messages(request, id=None):
    if id == None:
        messages = m.SupportMessages.objects.filter(user=request.user).filter(reply=True).filter(delivered=False)
    else:
        messages = m.SupportMessages.objects.filter(user=User.objects.filter(id=id)).filter(reply=False).filter(delivered=False)
    data = serializers.serialize("json", messages)
    messages.update(delivered=True)
    return HttpResponse(data, content_type='application/json')
