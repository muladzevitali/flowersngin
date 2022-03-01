from django import forms
from apps.user import models


class ContactForm(forms.ModelForm):
    class Meta:
        model = models.Contact
        fields = '__all__'

    def send_email(self):
        print("sending email", self.cleaned_data)
