from django import forms


class MailchimpSubscribeForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=100)
