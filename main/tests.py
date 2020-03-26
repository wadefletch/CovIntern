from django.test import TestCase

from .forms import EMPTY_EMAIL_ERROR, INVALID_EMAIL_ERROR, MailchimpSubscribeForm
from .models import SavedEmail

class IndexViewTest(TestCase):
    def test_uses_index_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'main/index.html')

    def test_redirect_on_email_submission(self):
        response = self.client.post('/', data={'email': 'wbfletch@gmail.com'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/jobs/')

    def test_index_page_uses_mailchimp_form(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], MailchimpSubscribeForm)

    def test_form_validation_for_blank_email(self):
        form = MailchimpSubscribeForm(data={'email': ''})
        self.assertEqual(form.errors['email'], [EMPTY_EMAIL_ERROR])

    def test_form_validation_for_invalid_email(self):
        form = MailchimpSubscribeForm(data={'email': 'not_an_email'})
        self.assertEqual(form.errors['email'], [INVALID_EMAIL_ERROR])

    def test_form_validation_errors_are_sent_back_to_index_template(self):
        response = self.client.post('/', data={'email': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/index.html')


class AboutViewTest(TestCase):
    def test_uses_about_template(self):
        response = self.client.get('/about/')
        self.assertTemplateUsed(response, 'main/about.html')


class SavedEmailModelTest(TestCase):
    def test_string_representation(self):
        saved_email = SavedEmail.objects.create(email='admin@covintern.com')
        self.assertEqual(str(saved_email), saved_email.email)
