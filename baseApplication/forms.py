from django import forms
from django.core.exceptions import ValidationError
from .models import Profile, Answer, Question


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
    __username_max_length = 64
    __password_max_length = 64
    username = forms.CharField(max_length=__username_max_length)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'maxlength': __password_max_length}))
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
    __help_text = "Maximum " + str(__text_max_length) + " symbols"
    text = forms.CharField(widget=forms.Textarea(
        attrs={'rows': '15', 'placeholder': 'Input your answer here', 'maxlength': __text_max_length}), label="",
        help_text=__help_text)

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


class QuestionForm(forms.ModelForm):
    __text_max_length = 4096
    __title_max_length = 128
    __tags_max_length = 128
    __help_text = "Maximum " + str(__text_max_length) + " symbols"
    __help_title = "Maximum " + str(__title_max_length) + " symbols"
    __help_tag = "Maximum " + str(__tags_max_length) + " symbols"

    text = forms.CharField(widget=forms.Textarea(
        attrs={'rows': '15', 'placeholder': 'Input your question here', 'maxlength': __text_max_length}),
        label="Questions",
        help_text=__help_text)

    title = forms.CharField(max_length=__title_max_length, help_text=__help_title,
                            widget=forms.TextInput(attrs={'placeholder': 'Title', 'rows': '1'}))

    tags = forms.CharField(max_length=__tags_max_length, help_text=__help_tag,
                           widget=forms.TextInput(attrs={'placeholder': 'Input tags through a space', 'rows': '1'}))

    def clean_text(self):
        data = self.cleaned_data["text"]
        if len(data) > self.__text_max_length:
            error_text = "Question is too long. Maximum " + str(self.__text_max_length) + " symbols required"
            raise ValidationError(error_text)
        if len(data) == 0:
            error_text = "Question is empty"
            raise ValidationError(error_text)
        return data

    def clean_title(self):
        data = self.cleaned_data["title"]
        if len(data) > self.__title_max_length:
            error_text = "Title is too long. Maximum " + str(self.__text_max_length) + " symbols required"
            raise ValidationError(error_text)
        if len(data) == 0:
            error_text = "Title is empty"
            raise ValidationError(error_text)
        return data

    def clean_tags(self):
        data = self.cleaned_data["tags"]
        if len(data) > self.__title_max_length:
            error_text = "Tags is too long. Maximum " + str(self.__tags_max_length) + " symbols required"
            raise ValidationError(error_text)
        return data

    class Meta:
        model = Question
        fields = ["title", "text"]
