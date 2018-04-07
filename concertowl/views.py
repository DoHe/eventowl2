from django.shortcuts import render

from concertowl.models import Event


def index(request):
    events = Event.objects.order_by('-date_time')
    return render(request, 'concertowl/index.html', {'events': events})
