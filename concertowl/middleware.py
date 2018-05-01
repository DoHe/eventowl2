import uuid

from django.contrib.auth import login
from django.contrib.auth.models import User
from geolite2 import geolite2
from ipware import get_client_ip

from concertowl.models import UserProfile

GEOIP_READER = geolite2.reader()


def session_user(get_response):
    def middleware(request):
        if not (request.user.is_authenticated or request.GET.get('uuid')):
            unique_id = request.session.get('id')
            if unique_id:
                user = User.objects.get(username=unique_id)
            else:
                new = False
                while not new:
                    unique_id = str(uuid.uuid4())
                    user, new = User.objects.get_or_create(username=unique_id)
                user.save()
                city = country = ''
                ip, is_routable = get_client_ip(request)
                if is_routable or True:
                    ip_info = GEOIP_READER.get(ip)
                    if ip_info is not None:
                        city = ip_info['city']
                        country = ip_info['country']
                UserProfile.objects.create(user=user, city=city, country=country).save()
                request.session['id'] = unique_id

            login(request, user)
        return get_response(request)

    return middleware
