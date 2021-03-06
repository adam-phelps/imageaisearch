from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class FormImageUpload(forms.Form):
    file = forms.FileField()

class UserCreationFormHidden(UserCreationForm):
    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs) 
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']