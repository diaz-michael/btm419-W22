from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field

# based on https://github.com/codingforentrepreneurs/Try-Django-3.2

from .models import order_form, order
class order_formForm(forms.ModelForm):
    error_css_class = 'error-field'
    required_css_class = 'required-field'
    # name = forms.CharField(help_text='This is your help! <a href="/contact">Contact us</a>')
    # descriptions = forms.CharField(widget=forms.Textarea(attrs={"rows": 3}))
    class Meta:
        model = order_form
        fields = ['dealershipID', 'salespersonID', 'id']
    
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


class orderForm(forms.ModelForm):
     
    class Meta:
        model = order
        fields = ['productID', 'discount', 'quantity', 'price']
        widgets = {
            'price': forms.TextInput(attrs={'readonly': True}),
        }
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
        # Formatting not working
        # helper = FormHelper()
        # helper.layout = Layout(
        #     Div(
        #         Field('productID', wrapper_class='col-md-12'),
        #         Field('discount', wrapper_class='col-md-4'),
        #         Field('quantity', wrapper_class='col-md-4'),  
        #         Field('price', wrapper_class='col-md-4'),
        #     css_class='form-row'))
        self.fields['productID'].label = 'Product'