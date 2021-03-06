from django import forms
from django.contrib.auth.models import User

from concertowl.helpers import get_or_none


class UserForm(forms.Form):
    city = forms.CharField(required=True)
    country = forms.CharField(required=True)
    username = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    password = forms.CharField(widget=forms.PasswordInput(), required=False)

    def _clean_no_duplication(self, data, field):
        if data and self.initial and field in self.changed_data and get_or_none(User, **{field: data}):
            raise forms.ValidationError("{} already exists".format(field.title()))
        return data

    def _clean_no_delete(self, field):
        data = self.cleaned_data[field]
        if self.initial.get(field) and not data:
            raise forms.ValidationError("You are not allowed to delete your {}".format(field), code='no_delete')
        return data

    def clean_password(self):
        return self._clean_no_delete('password')

    def clean_username(self):
        data = self._clean_no_delete('username')
        return self._clean_no_duplication(data, 'username')

    def clean_email(self):
        data = self._clean_no_delete('email')
        return self._clean_no_duplication(data, 'email')

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if self.errors.get('email') or self.errors.get('password'):
            return

        if email and not password:
            self.add_error('password', "You have to provide a password when signing up")

        if password and not email:
            self.add_error('email', "You have to provide an e-mail when signing up")
