from django.forms import ModelForm, widgets 
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Field
from .models import inspection

class inspectionForm(ModelForm):
    error_css_class = 'error-field'
    required_css_class = 'required-field'
    class Meta:
        model = inspection
        fields = ['claimID', 'vin', 'make', 'model', 'year', 'colour', 'status', 'scheduledDate', 'scheduledTime']
        widgets = {
            'status' : widgets.Select(),
            'scheduledDate': widgets.DateInput(attrs={'type': 'date'},),
            'scheduledTime': widgets.TimeInput(format = '%H:%M', attrs={'type': 'time'},)
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'claimID',
                'vin',
                'make',
                'model',
                'year',
                'colour',
                'status',
                'scheduledDate',
                'scheduledTime'
            ),
            Field('claimID', css_class='form-select'),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='button white')
            )
        )
        self.fields['vin'].label = 'VIN'
        self.fields['claimID'].label = 'Claim'
        self.fields['scheduledDate'].label = 'Scheduled Date'
        self.fields['scheduledTime'].label = 'Scheduled Time'