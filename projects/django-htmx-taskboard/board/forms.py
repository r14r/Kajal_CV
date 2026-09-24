from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "note"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "e.g. Build a portfolio page", "autofocus": True}),
            "note": forms.Textarea(attrs={"placeholder": "Optional details", "rows": 2}),
        }

    def clean_title(self):
        title = self.cleaned_data["title"].strip()
        if not title:
            raise forms.ValidationError("Please enter a task title.")
        return title
