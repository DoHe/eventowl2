import json

from concertowl.helpers import user_notifications


def notifications(request):
    if request.GET.get('uuid'):
        return {}
    is_manual = False
    try:
        is_manual = request.user.profile.manual
    except AttributeError:
        pass
    return {
        'notifications': json.dumps([n.to_json() for n in user_notifications(request.user)]),
        'is_manual': is_manual
    }
