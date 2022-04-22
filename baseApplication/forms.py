from django import forms
from django.core.exceptions import ValidationError
from .models import Profile, Answer


# @login_required

class RegistrationForm(forms.ModelForm):
    __password_min_length = 4
    __username_min_length = 6

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    field_order = ["username", "email", "password", "confirm_password", "first_name", "last_name", "profile_image"]

    def save(self, commit=True):
        profile = Profile(username=self.cleaned_data["username"], first_name=self.cleaned_data["first_name"],
                          last_name=self.cleaned_data["last_name"], email=self.cleaned_data["email"],
                          profile_image=self.cleaned_data["profile_image"])
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

    def clean_confirm_password(self):
        data = self.cleaned_data["confirm_password"]
        cleaned_data = super(RegistrationForm, self).clean()
        confirm_data = cleaned_data["password"]
        if len(data) < self.__password_min_length:
            error_text = "Password is too short. Minimum " + str(self.__password_min_length) + " symbols required"
            raise ValidationError(error_text)
        if data != confirm_data:
            error_text = "Passwords do not match"
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
        fields = ["username", "password", "email", "profile_image", "first_name", "last_name"]


class LoginForm(forms.Form):
    __password_min_length = 4
    __username_min_length = 6
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
    field_order = ["username", "password"]

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


class AnswerForm(forms.ModelForm):
    __text_max_length = 4096
    text = forms.CharField(widget=forms.Textarea(attrs={'rows': '15'}))

    def clean_text(self):
        data = self.cleaned_data["text"]
        if len(data) > self.__text_max_length:
            error_text = "Answer is too long. Maximum " + str(self.__text_max_length) + " symbols required"
            raise ValidationError(error_text)
        if len(data) == 0:
            error_text = "Answer is empty"
            raise ValidationError(error_text)
        return data

    class Meta:
        model = Answer
        fields = ["text"]
