import json

from concertowl.helpers import user_notifications


def notifications(request):
    return {'notifications': json.dumps(user_notifications(request.user.id))}
