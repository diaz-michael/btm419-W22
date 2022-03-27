from django import forms

# based on https://github.com/codingforentrepreneurs/Try-Django-3.2

from .models import order_form, order
class order_formForm(forms.ModelForm):
    error_css_class = 'error-field'
    required_css_class = 'required-field'
    # name = forms.CharField(help_text='This is your help! <a href="/contact">Contact us</a>')
    # descriptions = forms.CharField(widget=forms.Textarea(attrs={"rows": 3}))
    class Meta:
        model = order_form
        fields = ['dealershipID', 'salespersonID']
    
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
        # self.fields['name'].label = ''
        # self.fields['name'].widget.attrs.update({'class': 'form-control-2'})
        #self.fields['dealershipID'].widget.attrs.update({'rows': '2'})
        #self.fields['salespersonID'].widget.attrs.update({'rows': '4'})


class orderForm(forms.ModelForm):
    class Meta:
        model = order
        fields = ['productID', 'discount', 'quantity']
