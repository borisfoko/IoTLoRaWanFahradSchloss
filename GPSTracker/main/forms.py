from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import User
from django.forms import EmailField
from .models import Tracker, Route, GPSPoint

class UserCreationForm(UserCreationForm):
    email = EmailField(label=("E-Mail:"), required=True,
        help_text=("Required."))

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class UserForm(forms.ModelForm):
    email = EmailField(label=("E-Mail:"), required=True,
                       help_text=("Required."))

    class Meta:
        model = User
        fields = ['email']


class AddForm(forms.ModelForm):

    device_name = forms.CharField(label='Device Name:', max_length=50)
    device_eui = forms.CharField(label='Device EUI:', max_length=50)

    class Meta:
        model = Tracker
        fields = ("device_name", "device_eui")
