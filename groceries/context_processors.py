import support.models as s


def message_notification(request):
    if request.user.is_anonymous:
        return {'message_notification': False}
    else:
        if s.SupportMessages.objects.filter(user=request.user).filter(reply=True).filter(delivered=False).count() > 0:
            return {'message_notification': True}
        else:
            return {'message_notification': False}
