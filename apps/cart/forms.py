from django import forms
from django.core import validators


class AddToCartForm(forms.Form):
    quantity = forms.IntegerField(validators=[validators.MinValueValidator(0, 'quantity must be non negative')])
