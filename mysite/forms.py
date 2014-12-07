from django import forms


from django.forms import ModelForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field
from crispy_forms.bootstrap import (
    PrependedText, PrependedAppendedText, FormActions)
from search.models import *



# Create the form class.
class PrevHomeSalesForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(PrevHomeSalesForm, self).__init__(*args,**kwargs)
        self.fields['elementary'].label = "Elementary School Rating: 1-10"
        self.fields['middle'].label = "Middle School Rating: 1-10"
        self.fields['high'].label = "High School Rating: 1-10"
        
    def clean(self):
        cleaned_data = self.cleaned_data
        id = cleaned_data.get('id')
        
        #if not id:
        #    raise forms.ValidationError("Must specify an ID")
        
        return super(PrevHomeSalesForm,self).clean()
    
    
    class Meta:
        model = PrevHomeSales
        
    id = forms.IntegerField(widget=forms.HiddenInput()) #need this for the model to update properly
    #TODO: Rename elementary school to a rating
    
    #middle.label = "Middle School rating 1-10"
    #high.label = "High School rating 1-10"
    
    HOME_TYPE_CHOICES = (('Single Family Residence', 'Single Family Residence'), ('Condo/Townhouse', 'Condo/Townhouse'), )
    property_type = forms.TypedChoiceField(choices=HOME_TYPE_CHOICES,
                                            widget=forms.Select,
                                            empty_value = None,
                                            )
    helper = FormHelper()
    helper.form_method = 'POST'
    helper.layout = Layout(
        Field('property_type', css_class='input-sm'),
        Field('address', css_class='input-sm'),
        Field('city', css_class='input-sm'),
        Field('state', css_class='input-sm'),
        Field('zipcode', css_class='input-sm'),
        Field('beds', css_class='input-sm'),
        Field('baths', css_class='input-sm'),
        Field('sqft', css_class='input-sm'),
        Field('lot_size', css_class='input-sm'),
        Field('year_built', css_class='input-sm'),
        #HTML("""<p>We use notes to get better, <strong>please help us {{ username }}</strong></p>"""),
        Field('high',  css_class='input-sm'),
        Field('middle',  css_class='input-sm'),
        Field('elementary',  css_class='input-sm'),
        
        
        
        #bunch of fields hidden for now
        Field('last_sale_date', type="hidden"),
        Field('id', type="hidden"),
        Field('user_input', type="hidden"),
        Field('latitude', type="hidden"),
        Field('longitude', type="hidden"),
        Field('image_url', type="hidden"),
        Field('remodeled', type="hidden"),
        Field('sale_price', type="hidden"),
        Field('last_zestimate', type="hidden"),
        Field('exterior_rating', type="hidden"),
        Field('interior_rating', type="hidden"),

    )
    helper.add_input(Submit('Submit', 'Submit', css_class='btn-primary'))

class LeadGenUserForm(ModelForm):
    class Meta:
        model = LeadGenUser
        exclude = ('phone_number',)
    INQUIRY_REASON_CHOICES = (('Selling', 'Selling'), ('Buying', 'Buying'), ('Re-financing', 'Re-financing'), ('Curious', 'Just curious'))
    
    inquiry_reason = forms.TypedChoiceField(
                     choices=INQUIRY_REASON_CHOICES, widget=forms.RadioSelect, empty_value = None,
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