from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm
from django.core import mail
from eventex.subscriptions.models import Subscription


class SubscriptionGet(TestCase):
    def setUp(self):
        self.resp = self.client.get('/inscricao/')
        
    def test_get(self):
        """Get /inscricao/ must return status code 200"""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """Must use subscriptons/subscription_form.html"""
        self.assertTemplateUsed(self.resp, 'subscriptions/subscription_form.html')

    def test_html(self):
        """Html must contain input tags"""
        tags = (
            ('<form',1),
            ('<input',6),
            ('type="text"',3),
            ('type="email"',1),
            ('type="submit"',1),
        )
        for text, count in tags:
            with self.subTest():
                self.assertContains(self.resp, text, count)
    
    def test_csrf(self):
        """Html must contain csrf"""
        self.assertContains(self.resp, 'csrfmiddleware')


class SubscriptionPostValid(TestCase):
    def setUp(self):
        data = dict(name='Milton Filho', cpf='12345678901',
                    email='mosfilho@gmail.com', phone='869999999999')
        self.resp = self.client.post('/inscricao/', data)
    
    def test_post(self):
        """Valid POST should rerirect to /inscricao/"""
        self.assertEqual(302, self.resp.status_code)
    
    def test_send_subscription_email(self):
        self.assertEqual(1, len(mail.outbox))    

    def test_save_subscription(self):
        self.assertTrue(Subscription.objects.exists())


class SubscriptionPostInvalid(TestCase):
    def setUp(self):
        self.resp = self.client.post('/inscricao/')

    def test_post(self):
        """Invalid POST should not redirect"""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'subscriptions/subscription_form.html')
    
    def test_has_form(self):
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_errors(self):
        form = self.resp.context['form']
        self.assertTrue(form.errors)

    def test_dont_save_subscription(self):
        self.assertFalse(Subscription.objects.exists())


class SubscriptionSuccessMessage(TestCase):
    def setUp(self):
        data = dict(name='Milton Filho', cpf='03831156395',
                    email='mosfilho@gmail.com', phone='86999102776')
        self.resp = self.client.post('/inscricao/', data, follow=True)

    def test_message(self):
        self.assertContains(self.resp, 'Inscrição realizada com sucesso!')
