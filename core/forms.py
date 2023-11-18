from ckeditor.widgets import CKEditorWidget
from django import forms
from .models import OpenAICommand

CATEGORY_CHOICES = [
        ('Code Review', 'Code Review'),
        ('Automate', 'Automate'),
        ('Tester', 'Tester'),
    ]

class OpenAICommandForm(forms.ModelForm):

    category = forms.ChoiceField(
        choices=CATEGORY_CHOICES
    )

    class Meta:
        model = OpenAICommand
        fields = ['title', 'prompt', 'response', 'category', 'version']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'prompt': forms.CharField(widget=forms.Textarea(attrs={'id': 'prompt'})),
            'response': forms.CharField(widget=forms.Textarea(attrs={'id': 'response'})),
            'version': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': 'Title',
            'prompt': 'Code',
            'responnse': 'Response',
            'version': 'Version'
        }