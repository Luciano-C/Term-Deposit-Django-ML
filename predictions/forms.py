from django import forms
from .models import Client




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

class UploadClientsForm(forms.Form):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'form-control mb-2 mt-3'}), label='')
    
    def clean_file(self):
        file = self.cleaned_data.get('file')
        ext = file.name.split('.')[-1].lower()
        
        # Validate if file is csv
        if ext not in ['csv'] :
            raise forms.ValidationError("Only CSV files are allowed.")
        
        # Validate if the separator character is ";"
        # Read the first line of the file
        first_line = file.readline().decode()
        if ';' not in first_line:
            raise forms.ValidationError("CSV file must use ';' as separator.")
               # Validate number of the columns in csv file
        
        # Validate number of the columns in csv file
        first_line_as_list = first_line.split(';')
        if len(first_line_as_list) != 17:
            raise forms.ValidationError("CSV file must have 17 columns.")


        return file
  