from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import CustomerProfile, Review


class SignUpForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = CustomerProfile
        fields = ('phone', 'address', 'city', 'postal_code')
        widgets = {'address': forms.TextInput(attrs={'autocomplete': 'street-address'})}


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('rating', 'title', 'body')
        widgets = {
            'rating': forms.Select(choices=[(value, f'{value} stars') for value in range(5, 0, -1)]),
            'body': forms.Textarea(attrs={'rows': 4}),
        }


class CheckoutForm(forms.Form):
    address = forms.CharField(max_length=220, label='Street address')
    city = forms.CharField(max_length=100)
    postal_code = forms.CharField(max_length=20, label='Postal code')
    phone = forms.CharField(max_length=30)
    notes = forms.CharField(max_length=300, required=False, widget=forms.Textarea(attrs={'rows': 3}))