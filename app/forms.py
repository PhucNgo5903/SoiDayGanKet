from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.contrib.auth.models import User
from .models import Donor, Volunteer


class LoginForm(AuthenticationForm):
    username = UsernameField(required=True, widget=forms.TextInput(attrs={'autofocus' : 'True',
    'class': 'form-control', 'placeholder': 'username'}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'form-control',
    'placeholder': 'Password'}))



class UserForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Enter Password"}),
    )
    password2 = forms.CharField(
        label="Confirm Password (again)",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Enter Password Again"}),
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "password1", "password2"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter First Name"}),
            "last_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter Last Name"}),
            "username": forms.TextInput(attrs={"class": "form-control", "placeholder": "Username"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email ID"}),
        }

class DonorSignupForm(forms.ModelForm):
    userpic = forms.ImageField(widget=forms.ClearableFileInput(attrs={"class": "form-control"}))

    class Meta:
        model = Donor
        fields = ["contact", "userpic"]
        widgets = {
            "contact": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Contact Number"}),
        }

class VolunteerSignupForm(forms.ModelForm):
    userpic = forms.ImageField(widget=forms.ClearableFileInput(attrs={"class": "form-control"}))

    class Meta:
        model = Volunteer
        fields = ["contact", "userpic"]
        widgets = {
            "contact": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Contact Number"}),
        }


