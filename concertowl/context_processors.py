from concertowl.helpers import user_notifications


def notification_count(request):
    return {'num_notifications': len(user_notifications(request.user.id))}
