import uuid

from django.contrib.auth import login
from django.contrib.auth.models import User
from geolite2 import geolite2
from ipware import get_client_ip
import user_agents

from concertowl.models import UserProfile

GEOIP_READER = geolite2.reader()


def _create_profile(user, request, manual=False, unique_id=None):
    country = 'germany'
    city = 'berlin'
    ip, is_routable = get_client_ip(request)
    if is_routable:
        ip_info = GEOIP_READER.get(ip)
        if ip_info is not None:
            try:
                city = ip_info['city']['names']['en']
                country = ip_info['country']['names']['en']
            except KeyError:
                pass
    if unique_id:
        UserProfile.objects.create(user=user, city=city.lower(), country=country.lower(),
                                   manual=manual, uuid=unique_id).save()
    else:
        UserProfile.objects.create(user=user, city=city.lower(), country=country.lower(), manual=manual).save()


def session_user(get_response):
    def middleware(request):
        if request.GET.get('uuid'):
            return get_response(request)

        if user_agents.parse(request.META['HTTP_USER_AGENT']).is_bot:
            return get_response(request)

        if request.user.is_authenticated:
            if not hasattr(request.user, 'profile'):
                _create_profile(request.user, request, True)
            return get_response(request)

        unique_id = request.session.get('id')
        if unique_id:
            user = User.objects.get(profile__uuid=unique_id)
        else:
            new = False
            while not new:
                unique_id = str(uuid.uuid4())
                user, new = User.objects.get_or_create(username=unique_id)
            user.save()
            _create_profile(user, request, False, unique_id)
            request.session['id'] = unique_id

        login(request, user)
        return get_response(request)

    return middleware
