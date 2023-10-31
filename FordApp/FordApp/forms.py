from django import forms
from SoftwareSetLookupTool.models import BuildUrl
class BuildUrlForm(forms.ModelForm):
    class Meta:
        model=BuildUrl
        fields=["build_url"]