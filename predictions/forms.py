from django import forms
from .models import Client
import pandas as pd




class ClientForm(forms.ModelForm):
    class Meta():
        model = Client
        fields = [
                'full_name',
                'age',
                'job',
                'marital',
                'education',
                'default',
                'balance',
                'housing',
                'loan',
                'contact',
                'day',
                'month',
                'duration',
                'campaign',
                'pdays',
                'previous',
                'poutcome'
            ]
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Write a name', "class": "form-control mb-2"}),
            'age': forms.NumberInput(attrs={"class": "form-control mb-2"}),
            'job': forms.Select(attrs={"class": "form-control mb-2"}),
            'marital': forms.Select(attrs={"class": "form-control mb-2"}),
            'education': forms.Select(attrs={"class": "form-control mb-2"}),
            'default': forms.Select(attrs={"class": "form-control mb-2"}),
            'balance': forms.NumberInput(attrs={"class": "form-control mb-2"}),
            'housing': forms.Select(attrs={"class": "form-control mb-2"}),
            'loan': forms.Select(attrs={"class": "form-control mb-2"}),
            'contact': forms.Select(attrs={"class": "form-control mb-2"}),
            'day': forms.NumberInput(attrs={"class": "form-control mb-2"}),
            'month': forms.Select(attrs={"class": "form-control mb-2"}),
            'duration': forms.NumberInput(attrs={"class": "form-control mb-2"}),
            'campaign': forms.NumberInput(attrs={"class": "form-control mb-2"}),
            'pdays': forms.NumberInput(attrs={"class": "form-control mb-2"}),
            'previous': forms.NumberInput(attrs={"class": "form-control mb-2"}),
            'poutcome': forms.Select(attrs={"class": "form-control mb-2"}),
        }


  