from django import forms

from .models import inspection

class inspectionForm(forms.ModelForm):
    error_css_class = 'error-field'
    required_css_class = 'required-field'
    class Meta:
        model = inspection
        fields = ['claimID', 'vin', 'make', 'model', 'year', 'colour', 'status', 'scheduledDate']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # django-crispy-forms
        for field in self.fields:
            new_data = {
                "placeholder": f'order_form {str(field)}',
                "class": 'form-control'
            }
            self.fields[str(field)].widget.attrs.update(
                new_data
            )
        
        self.fields['claimID'].label = 'Claim'
        self.fields['scheduledDate'].label = 'Scheduled Date'