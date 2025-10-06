from django import forms
from .models import Label

class LabelForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
        }
        labels = {
            "name": "Имя",
        }
