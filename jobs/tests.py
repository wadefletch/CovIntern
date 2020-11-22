import datetime

from dateutil.relativedelta import relativedelta
from django.template import Context, Template
from django.test import LiveServerTestCase, TestCase
from django.urls import reverse
from django.utils import timezone
from selenium import webdriver

from .models import Category, Company, Job


class CompanyModelTests(TestCase):
    def test_string_representation(self):
        c = Company(
            name='Google',
            location='Mountain View, CA',
            url='google.com'
        )

        self.assertEqual(str(c), c.name)

    def test_verbose_name_plural(self):
        self.assertEqual(str(Company._meta.verbose_name_plural), 'companies')

    def test_formatted_url_http(self):
        c = Company(
            name='Google',
            location='Mountain View, CA',
            url='http://google.com'
        )

        self.assertEqual(c.formatted_url, 'google.com')

    def test_formatted_url_https(self):
        c = Company(
            name='Google',
            location='Mountain View, CA',
            url='https://google.com'
        )

        self.assertEqual(c.formatted_url, 'google.com')

    def test_formatted_url_no_protocol(self):
        c = Company(
            name='Google',
            location='Mountain View, CA',
            url='google.com'
        )

        self.assertEqual(c.formatted_url, 'google.com')


class CategoryModelTests(TestCase):
    def test_string_representation(self):
        c = Category(
            name='Data Science'
        )

        self.assertEqual(str(c), c.name)

    def test_verbose_name_plural(self):
        self.assertEqual(str(Category._meta.verbose_name_plural), 'categories')


class JobModelTests(TestCase):
    def setUp(self):
        self.j = Job.objects.create(
            title='Data Science Intern',
            company=Company.objects.create(
                name='Google',
                location='Mountain View, CA',
                url='google.com'
            ),
            application_link='google.com',
            category=Category.objects.create(
                name='Data Science'
            ),
            description='Job Description Text',
            qualifications='Job Qualifications Here'
        )

    def test_string_representation(self):
        self.assertEqual(str(self.j), f'{self.j.title} @ {self.j.company.name}')


class UpToTemplateTagTests(TestCase):
    def test_rendered(self):
        context = Context({'posted': timezone.now() - relativedelta(hours=22, minutes=20)})
        template_to_render = Template(
            "{% load upto %}"
            "<p>Posted {{ posted|timesince|upto:', ' }} ago</p>"
        )
        rendered_template = template_to_render.render(context)
        self.assertInHTML('<p>Posted 22 hours ago</p>', rendered_template)


class JobListViewTests(TestCase):
    def test_uses_list_template(self):
        response = self.client.get('/jobs/')
        self.assertTemplateUsed(response, 'jobs/list.html')

    def test_featured_postings_first(self):
        c = Company.objects.create(
            name='Google',
            location='Mountain View, CA',
            url='google.com'
        )
        ca = Category.objects.create(
            name='Data Science'
        )
        j1 = Job.objects.create(
            title='Featured Intern',
            company=c,
            application_link='google.com',
            category=ca,
            description='Job Description Text',
            qualifications='Job Qualifications Here',
            featured=True
        )
        j2 = Job.objects.create(
            title='Normal Intern',
            company=c,
            application_link='google.com',
            category=ca,
            description='Job Description Text',
            qualifications='Job Qualifications Here',
            featured=False
        )

        response = self.client.get(reverse('jobs:list'))
        self.assertQuerysetEqual(response.context['job_list'],
                                 ['<Job: Featured Intern @ Google>', '<Job: Normal Intern @ Google>'])

    def test_hide_deadline_passed(self):
        c = Company.objects.create(
            name='Google',
            location='Mountain View, CA',
            url='google.com'
        )
        ca = Category.objects.create(
            name='Data Science'
        )
        j1 = Job.objects.create(
            title='Application Still Open Intern',
            company=c,
            application_link='google.com',
            application_deadline=datetime.datetime.now() + datetime.timedelta(weeks=1),
            category=ca,
            description='Job Description Text',
            qualifications='Job Qualifications Here',
            featured=True
        )
        j2 = Job.objects.create(
            title='Application Closed Intern',
            company=c,
            application_link='google.com',
            application_deadline=datetime.datetime.now() - datetime.timedelta(weeks=1),
            category=ca,
            description='Job Description Text',
            qualifications='Job Qualifications Here',
            featured=False
        )
        j3 = Job.objects.create(
            title='Application Closing Today Intern',
            company=c,
            application_link='google.com',
            application_deadline=datetime.datetime.combine(datetime.date.today(), datetime.datetime.max.time()),
            category=ca,
            description='Job Description Text',
            qualifications='Job Qualifications Here',
            featured=True
        )

        response = self.client.get(reverse('jobs:list'))
        print(response.context['job_list'])
        self.assertQuerysetEqual(response.context['job_list'], ['<Job: Application Closing Today Intern @ Google>',
                                                                '<Job: Application Still Open Intern @ Google>'])


class AboutViewTests(TestCase):
    def test_uses_about_template(self):
        response = self.client.get('/jobs/about/')
        self.assertTemplateUsed(response, 'jobs/about.html')


class JobCreateFormTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test Category')

    def test_can_create_job(self):
        data = {
            'job-title': 'Test Intern',
            'job-category': self.category.id,
            'job-description': 'This is the job description.',
            'job-qualifications': 'These are the relevant qualifications.',
            'job-application_link': 'https://covintern.com',
            'job-application_deadline': '2020-10-20T10:12',
            'job-contact_email': 'wade@covintern.com',
            'company-name': 'CovIntern',
            'company-location': 'Columbia, SC',
            'company-url': 'http://covintern.com',
        }
        resp = self.client.post(reverse('jobs:create'), data=data)
        self.assertEqual(resp.status_code, 302)
