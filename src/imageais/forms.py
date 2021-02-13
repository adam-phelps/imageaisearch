from django import forms

class FormImageUpload(forms.Form):
    file = forms.FileField()