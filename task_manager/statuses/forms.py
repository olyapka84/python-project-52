from django import forms
from .models import Status


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ["name"]
        labels = {"name": "Name"}
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
        }
