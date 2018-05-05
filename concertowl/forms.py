from django import forms

from concertowl.helpers import cities, countries


class UserForm(forms.Form):
    city = forms.ChoiceField(choices=[('{}_{}'.format(c.name.lower(), c.country.name.lower()), c.name)
                                      for c in cities()])
    country = forms.ChoiceField(choices=[(c.name.lower(), c.name) for c in countries()])
    username = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    password = forms.CharField(widget=forms.PasswordInput(), required=False)
