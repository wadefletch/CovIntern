from collections import OrderedDict
import datetime
from betterforms.multiform import MultiModelForm
from django import forms
from django.forms import ModelForm

from .models import Company, Job


class CompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Dunder Mifflin Incorporated'}),
            'location': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Scranton, PA'}),
            'url': forms.URLInput(attrs={'class': 'input', 'placeholder': 'https://'}),
        }


class JobForm(ModelForm):
    class Meta:
        model = Job
        fields = ('title', 'application_link', 'application_deadline', 'category', 'description', 'qualifications', 'contact_email')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Software Engineering Remote Intern'}),
            'description': forms.Textarea(attrs={'class': 'textarea', 'rows': 6}),
            'qualifications': forms.Textarea(attrs={'class': 'textarea', 'rows': 6}),
            'application_link': forms.URLInput(attrs={'class': 'input', 'placeholder': 'https://'}),
            'application_deadline': forms.DateTimeInput(attrs={'class': 'input', 'type': 'datetime-local'}),
            'contact_email': forms.EmailInput(attrs={'class': 'input', 'placeholder': 'your@email.com'})
        }


class JobCreationMultiForm(MultiModelForm):
    form_classes = OrderedDict([
        ('company', CompanyForm),
        ('job', JobForm),
    ])

    def save(self, commit=True):
        objects = super(JobCreationMultiForm, self).save(commit=False)

        if commit:
            company = objects['company']
            company.save()
            job = objects['job']
            job.company = company
            job.save()

        return objects
