from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser


class PhoneLoginForm(forms.Form):    
    username = forms.CharField(max_length=150, label="Username")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    phone_number = forms.RegexField(
        regex=r'^\+?\d{9,15}$', 
        max_length=15, 
        label='Telefon raqam', 
        error_messages={"invalid": "Telefon raqamni to'g'ri formatda kiriting (+998901234567)."})
    

class RegistrationForm(UserCreationForm):
    phone_number = forms.RegexField(
        regex=r'^\+?\d{9,15}$',
        label='Telefon raqam',
        error_messages={'invalid': "Telefon raqamni to'g'ri formatda kiriting (+998901234567)"}
    )

    class Meta:
        model = CustomUser
        fields = ("username", "phone_number", "password1", "password2")