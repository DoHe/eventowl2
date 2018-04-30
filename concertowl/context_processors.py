import json

from concertowl.helpers import user_notifications


def notifications(request):
    if request.GET.get('uuid'):
        return {}
    return {'notifications': json.dumps(user_notifications(request.user.id))}
