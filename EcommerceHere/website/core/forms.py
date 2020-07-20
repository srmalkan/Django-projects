from django import forms
from django.contrib.auth.models import User
from .models import Reviews
from django_countries.fields import CountryField

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password',
    widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password',
    widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

class ReviewsForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = ('body',)
        widgets ={
            "body":forms.Textarea(attrs={"class":"form-control"})
        }

payment_choices = (
    ('S','Stripe'),
    ('P','PayPal'),
)

state_choices = (
    ('maharashtra','maharashtra'),
    ('gujrat','gujrat'),
    ('Madhya Pradesh','Madhya Pradesh'),
    ('Rajasthan','Rajasthan'),
    ('Punjab','Punjab')
)

class CheckoutForm(forms.Form):
    Address_1 = forms.CharField(max_length=200)
    Address_2 = forms.CharField(max_length=200,required=False)
    state = forms.ChoiceField(choices=state_choices)
    zipCode = forms.CharField()
    same_billing_address = forms.BooleanField(widget=forms.CheckboxInput(),required=False)
    save_info = forms.BooleanField(widget=forms.CheckboxInput(),required=False)
    payment_option = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class':'form-check-input'}),choices=payment_choices,)


