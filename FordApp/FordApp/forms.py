from django import forms

class BuildUrlForm(forms.Form):
    build_url=forms.CharField(max_length=256)
