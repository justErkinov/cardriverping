from django import forms
class PhoneLoginForm(forms.Form):
    
    username = forms.CharField(max_length=150, label="Username")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    phone_number = forms.CharField(max_length=15, label="Telefon raqam")