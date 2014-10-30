from django import forms


from django.forms import ModelForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field
from crispy_forms.bootstrap import (
    PrependedText, PrependedAppendedText, FormActions)
from search.models import *

CHOICES = (('1', 'First',), ('2', 'Second',))


# Create the form class.
class TargetHomeForm(ModelForm):
    class Meta:
        model = PrevHomeSales
    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('Submit', 'Submit', css_class='btn-primary'))

class LeadGenUserForm(ModelForm):
    class Meta:
        model = LeadGenUser
        exclude = ('phone_number',)
    YESNO_CHOICES = (('Selling', 'Selling'), ('Buying', 'Buying'), ('Re-financing', 'Re-financing'), ('Curious', 'Just curious'))
    inquiry_reason = forms.TypedChoiceField(
                     choices=YESNO_CHOICES, widget=forms.RadioSelect, empty_value = None,
                     )
    inquiry_reason.label = 'Optimize report for:'

    helper = FormHelper()
    helper.form_method = 'POST'
    #helper.form_class = 'form-special' 
    helper.layout = Layout(
        Field('full_name', css_class='input-sm'),
        Field('email_address', css_class='input-sm'),
        Field('inquiry_reason', style="padding-left: 20px", css_class='form-special'),
    )

    helper.add_input(Submit('Submit', 'Get Your Report', css_class="btn btn-lg btn-success"))


#
#class SimpleForm(forms.Form):
#    username = forms.CharField(label="Username", required=True)
#    password = forms.CharField(
#        label="Password", required=True, widget=forms.PasswordInput)
#    remember = forms.BooleanField(label="Remember Me?")
#
#    helper = FormHelper()
#    helper.form_method = 'POST'
#    helper.add_input(Submit('login', 'login', css_class='btn-primary'))
#
#class CartForm(forms.Form):
#    item = forms.CharField()
#    quantity = forms.IntegerField(label="Qty")
#    price = forms.DecimalField()
#
#    helper = FormHelper()
#    helper.form_method = 'POST'
#    helper.layout = Layout(
#        'item',
#        PrependedText('quantity', '#'),
#        PrependedAppendedText('price', '$', '.00'),
#        FormActions(Submit('login', 'login', css_class='btn-primary'))
#    )
#
#
#class CreditCardForm(forms.Form):
#    fullname = forms.CharField(label="Full Name", required=True)
#    card_number = forms.CharField(label="Card", required=True, max_length=16)
#    expire = forms.DateField(label="Expire Date", input_formats=['%m/%y'])
#    ccv = forms.IntegerField(label="ccv")
#    notes = forms.CharField(label="Order Notes", widget=forms.Textarea())
#
#    helper = FormHelper()
#    helper.form_method = 'POST'
#    helper.form_class = 'form-horizontal'
#    helper.label_class = 'col-sm-2'
#    helper.field_class = 'col-sm-4'
#    helper.layout = Layout(
#        Field('fullname', css_class='input-sm'),
#        Field('card_number', css_class='input-sm'),
#        Field('expire', css_class='input-sm'),
#        Field('ccv', css_class='input-sm'),
#        Field('notes', rows=3),
#        FormActions(Submit('purchase', 'purchase', css_class='btn-primary'))
#    )