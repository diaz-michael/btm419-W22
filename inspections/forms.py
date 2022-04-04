from django.forms import ModelForm, widgets
from crispy_forms.helper import FormHelper
from .models import inspection, claim, warranty

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
        #using kwargs
        user = kwargs.pop('user', None)
        edit = kwargs.pop('edit', None)
        super(inspectionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        
        if user.is_staff == False:
            self.fields['claimID'].queryset = claim.objects.filter(warrantyID__customerID__email = user.email)
            print("not a staff")

            if edit:
                self.fields['vin'].widget.attrs['readonly'] = True
                self.fields['colour'].widget.attrs['readonly'] = True
                self.fields['year'].widget.attrs['readonly'] = True
                self.fields['make'].widget.attrs['readonly'] = True
                self.fields['model'].widget.attrs['readonly'] = True        

        self.fields['vin'].label = 'VIN'
        self.fields['claimID'].label = 'Claim'
        self.fields['scheduledDate'].label = 'Scheduled Date'
        self.fields['scheduledTime'].label = 'Scheduled Time'