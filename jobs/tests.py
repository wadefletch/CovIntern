from dateutil.relativedelta import relativedelta
from django.template import Context, Template
from django.test import TestCase
from django.utils import timezone

from .models import Category, Company, Job


class CompanyModelTest(TestCase):
    def test_string_representation(self):
        c = Company(
            name='Google',
            location='Mountain View, CA',
            url='google.com'
        )

        self.assertEqual(str(c), c.name)

    def test_verbose_name_plural(self):
        self.assertEqual(str(Company._meta.verbose_name_plural), "companies")

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


class CategoryModelTest(TestCase):
    def test_string_representation(self):
        c = Category(
            name='Data Science'
        )

        self.assertEqual(str(c), c.name)

    def test_verbose_name_plural(self):
        self.assertEqual(str(Category._meta.verbose_name_plural), "categories")


class JobModelTest(TestCase):
    def setUp(self):
        self.j = Job.objects.create(
            title='Data Science Intern',
            company=Company.objects.create(
                name='Google',
                location='Mountain View, CA',
                url='google.com'
            ),
            hours_per_week=30,
            application_link='google.com',
            category=Category.objects.create(
                name='Data Science'
            ),
            description='Job Description Text',
            qualifications='Job Qualifications Here'
        )

    def test_string_representation(self):
        self.assertEqual(str(self.j), f'{self.j.title} @ {self.j.company.name}')


class UpToTemplateTagTest(TestCase):
    def test_rendered(self):
        context = Context({'posted': timezone.now() - relativedelta(hours=22, minutes=20)})
        template_to_render = Template(
            "{% load upto %}"
            "<p>Posted {{ posted|timesince|upto:',' }} ago</p>"
        )
        rendered_template = template_to_render.render(context)
        self.assertInHTML('<p>Posted 22 hours ago</p>', rendered_template)
