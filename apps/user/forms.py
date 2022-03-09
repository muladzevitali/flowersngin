from django import forms
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from apps.user import models


class ContactForm(forms.ModelForm):
    class Meta:
        model = models.Contact
        fields = '__all__'

    def send_email(self):
        subject = 'Contact via flowersngin'
        message = render_to_string('mail/contact.html', self.cleaned_data)
        email = EmailMessage(subject, message, to=[settings.EMAIL_CONTACT_FORM_RECEIVER])
        email.send()
