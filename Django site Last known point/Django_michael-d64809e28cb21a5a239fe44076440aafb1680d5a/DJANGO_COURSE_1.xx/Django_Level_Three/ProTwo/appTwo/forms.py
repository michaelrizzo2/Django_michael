<<<<<<< HEAD
from django import forms
from appTwo.models import User

class NewUserForm(forms.ModelForm):
    class Meta():
        model = User
        fields = '__all__'
=======
from django import forms
from appTwo.models import User

class NewUserForm(forms.ModelForm):
    class Meta():
        model = User
        fields = '__all__'
>>>>>>> ac0e51a1fa64a5efaf8858bce7f5480528a7fd3e
