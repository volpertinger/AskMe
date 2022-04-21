from django import forms
from django.core.exceptions import ValidationError
from .models import Profile


#@login_required

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
    __password_min_length = 4
    __username_min_length = 6

    def clean_password(self):
        data = self.cleaned_data["password"]
        if len(data) < self.__password_min_length:
            error_text = "Password is too short. Minimum " + str(self.__password_min_length) + " symbols required"
            raise ValidationError(error_text)
        return data

    def clean_username(self):
        data = self.cleaned_data["username"]
        if len(data) < self.__username_min_length:
            error_text = "Username is too short. Minimum " + str(self.__username_min_length) + " symbols required"
            raise ValidationError(error_text)
        return data
