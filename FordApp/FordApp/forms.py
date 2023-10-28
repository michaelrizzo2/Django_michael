from django import forms

class BuildUrlForm(forms.Form):
    build_url=forms.CharField(max_length=256)

class LoginForm(forms.Form):
    username=forms.CharField(max_length=20)
    password=forms.CharField(max_length=25,widget=forms.PasswordInput())