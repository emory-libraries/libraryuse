from django import forms
from django.forms import ModelForm
from models import DataExport

class DataExportForm(ModelForm):
    #start_date = forms.DateField(label='Start Date', input_formats=['%d/%m/%Y', '%m/%d/%Y',], required=False)    
    #end_date =  forms.DateField(label='End Date', input_formats=['%d/%m/%Y', '%m/%d/%Y',], required=False)
    
    class Meta:
        model = DataExport
        widgets = {'date': forms.DateInput(attrs={'class': 'datePicker'})}
