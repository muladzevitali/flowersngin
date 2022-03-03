from django import forms

from .models import Order, Country


class OrderForm(forms.ModelForm):
    client_country = forms.ModelChoiceField(queryset=Country.objects.all())
    receiver_country = forms.ModelChoiceField(queryset=Country.objects.all(), required=False)

    class Meta:
        model = Order
        fields = ['company_name', 'btw_number',
                  'client_first_name', 'client_last_name', 'client_email', 'client_phone', 'client_street_name',
                  'client_house_number', 'client_bus', 'client_city', 'client_postalcode', 'client_country',
                  'receiver_first_name', 'receiver_last_name', 'receiver_street_name', 'receiver_house_number',
                  'receiver_bus', 'receiver_city', 'receiver_postalcode', 'receiver_country', 'order_note']
