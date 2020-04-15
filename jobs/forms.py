from collections import OrderedDict

from betterforms.multiform import MultiModelForm
from django import forms

from .models import Company, Job


class BulmaModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BulmaModelForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            field_type = type(visible.field.widget)
            if field_type in (forms.TextInput, forms.EmailInput, forms.URLInput):
                visible.field.widget.attrs['class'] = 'input'
            elif field_type in (forms.Textarea,):
                visible.field.widget.attrs['class'] = 'textarea'
                visible.field.widget.attrs['rows'] = 6

            if field_type in (forms.Select,):
                visible.field.empty_label = None

            if field_type in (forms.URLInput,):
                visible.field.widget.attrs['placeholder'] = 'https://'


class CompanyForm(BulmaModelForm):
    class Meta:
        model = Company
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Dunder Mifflin Incorporated'}),
            'location': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Scranton, PA'}),
            'url': forms.URLInput(attrs={'class': 'input', 'placeholder': 'https://'}),
        }


class JobForm(BulmaModelForm):
    class Meta:
        model = Job
        fields = ('title', 'application_link', 'category', 'description', 'qualifications', 'contact_email')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Software Engineering Remote Intern'}),
            'description': forms.Textarea(attrs={'class': 'textarea', 'rows': 6}),
            'qualifications': forms.Textarea(attrs={'class': 'textarea', 'rows': 6}),
            'application_link': forms.URLInput(attrs={'class': 'input', 'placeholder': 'https://'}),
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