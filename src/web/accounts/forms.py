from django import forms
from django.forms import ModelForm
from src.services.users.models import User


class UserProfileForm(ModelForm):

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name',
        ]


class PasswordForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput)