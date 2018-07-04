from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm
from django.core import mail


class SubscriptionPostValid(TestCase):
    def setUp(self):
        data = dict(name='Milton Filho', cpf='12345678901',
                    email='mosfilho@gmail.com', phone='869999999999')        
        self.client.post('/inscricao/', data)
        self.email = mail.outbox[0]    
    
    def test_subscription_email_subject(self):
        expect = 'Confirmação de inscrição'

        self.assertEqual(expect, self.email.subject)
    
    def test_subscription_email_from(self):
        expect = 'contato@eventex.com.br'

        self.assertEqual(expect, self.email.from_email)
    
    def test_subscription_email_to(self):
        expect = ['contato@eventex.com.br','mosfilho@gmail.com']

        self.assertEqual(expect, self.email.to)
    
    def test_subscription_email_body(self):
        contents = [
            'Milton Filho',
            '12345678901',
            '869999999999',
            'mosfilho@gmail.com'
        ]
        for content in contents:
            with self.subTest():
                self.assertIn(content, self.email.body)