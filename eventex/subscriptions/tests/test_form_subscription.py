from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm
from django.core import mail
from eventex.subscriptions.forms import SubscriptionForm


class SubscriptionFormTest(TestCase):
    def setUp(self):
        self.form = SubscriptionForm()

    def test_has_form(self):
        """Context must hace subscription form"""
        self.assertIsInstance(self.form, SubscriptionForm)
    
    def test_form_has_fields(self):
        """Form must have 4 fields"""
        self.assertSequenceEqual(['name','cpf','email','phone'], list(self.form.fields))