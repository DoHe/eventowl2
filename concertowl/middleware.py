import uuid

from django.contrib.auth import login
from django.contrib.auth.models import User


def session_user(get_response):
    def middleware(request):
        if not (request.user.is_authenticated or request.GET.get('uuid')):
            unique_id = request.session.get('id')
            if not unique_id:
                new = False
                while not new:
                    unique_id = str(uuid.uuid4())
                    user, new = User.objects.get_or_create(username=unique_id)
                user.save()
                request.session['id'] = unique_id
            else:
                user = User.objects.get(username=unique_id)
            login(request, user)
        return get_response(request)

    return middleware
