from cities_light.models import City, Country
from django import forms


class UserForm(forms.Form):
    city = forms.ChoiceField(choices=[(c.name.lower(), c.name) for c in City.objects.all()])
    country = forms.ChoiceField(choices=[(c.name.lower(), c.name) for c in Country.objects.all()])
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
