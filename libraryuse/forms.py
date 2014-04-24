from django import forms
from models import LibraryVisit
from django.db.models import Max, Min
from django.forms import ModelForm
from models import DataExport

class DataExportForm(ModelForm):
    
    class Meta:
        model = DataExport
        widgets = {'date': forms.DateInput(attrs={'class': 'datePicker'})}
    
    def __init__(self, *args, **kwargs):
        super(DataExportForm, self).__init__(*args, **kwargs)
        start_date = LibraryVisit.objects.all().aggregate(Min('visit_time'))
        end_date = LibraryVisit.objects.all().aggregate(Max('visit_time'))
        self.fields['start_date'].initial = start_date['visit_time__min']
        self.fields['end_date'].initial = end_date['visit_time__max']
