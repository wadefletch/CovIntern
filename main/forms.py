from django import forms

EMPTY_EMAIL_ERROR = "You can't subscribe with an empty email"
INVALID_EMAIL_ERROR = "You can only subscribe with a valid email"

class MailchimpSubscribeForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        max_length=100,
        error_messages={
            'required': EMPTY_EMAIL_ERROR,
            'invalid': INVALID_EMAIL_ERROR,
        }
    )
