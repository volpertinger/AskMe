from django import forms
from django.core.exceptions import ValidationError
from .models import Profile


# @login_required

class RegistrationForm(forms.ModelForm):
    __password_min_length = 4
    __username_min_length = 6

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    def save(self, commit=True):
        profile = Profile(username=self.cleaned_data["username"], first_name=self.cleaned_data["first_name"],
                          last_name=self.cleaned_data["last_name"], email=self.cleaned_data["email"])
        profile.set_password(self.cleaned_data["password"])
        if commit:
            profile.save()
        return profile

    def clean_username(self):
        data = self.cleaned_data["username"]
        if len(data) < self.__username_min_length:
            error_text = "Username is too short. Minimum " + str(self.__username_min_length) + " symbols required"
            raise ValidationError(error_text)
        return data

    def clean_password(self):
        data = self.cleaned_data["password"]
        if len(data) < self.__password_min_length:
            error_text = "Password is too short. Minimum " + str(self.__password_min_length) + " symbols required"
            raise ValidationError(error_text)
        return data

    class Meta:
        model = Profile
        fields = ["username", "password", "email", "profile_image"]


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
