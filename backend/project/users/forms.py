import datetime

import django.conf
import django.contrib.admin.widgets
import django.contrib.auth.forms
import django.contrib.auth.models
import django.forms

import core.forms
import users.models
import users.services


class SignUpForm(
    core.forms.BootstrapClassFormMixin,
    core.forms.BootstrapPlaceholderFormMixin,
    django.contrib.auth.forms.UserCreationForm,
):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.Meta.required:
            self.fields[field].required = True

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if users.models.User.objects.filter(username=username).exists():
            raise django.forms.ValidationError('Такое имя уже существует')

        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')

        normalized_email = users.services.generate_normalize_email(email)

        if users.models.User.objects.filter(email=normalized_email).exists():
            raise django.forms.ValidationError('Такая почта уже существует')

        return normalized_email

    class Meta:
        model = users.models.User
        fields = ('username', 'email', 'password1', 'password2')
        required = ('username', 'email', 'password1', 'password2')


class CustomAuthenticationForm(
    core.forms.BootstrapClassFormMixin,
    core.forms.BootstrapPlaceholderFormMixin,
    django.contrib.auth.forms.AuthenticationForm,
):
    username = django.forms.CharField(label='Логин или почта', max_length=254)

