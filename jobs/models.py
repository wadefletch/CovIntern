from django.db import models
from django.utils import timezone


class Company(models.Model):
    name = models.CharField(max_length=128)
    location = models.CharField(max_length=64, help_text='We know this is for a remote position, but applicants still want to know where a potential employer\'s HQ is located.')
    url = models.URLField(help_text="This should be the url of your company's homepage, not your job posting or application.")
    logo = models.ImageField()

    class Meta:
        verbose_name_plural = "companies"

    def __str__(self):
        return self.name

    @property
    def formatted_url(self):
        if self.url.startswith('http://'):
            return self.url[7:]
        elif self.url.startswith('https://'):
            return self.url[8:]
        else:
            return self.url


class Category(models.Model):
    name = models.CharField(max_length=64, verbose_name='Company Name')
    color = models.CharField(max_length=32, default='dark')

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Job(models.Model):
    title = models.CharField(max_length=128)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    application_link = models.CharField(max_length=256)
    application_deadline = models.DateTimeField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    qualifications = models.TextField(blank=True, null=True)
    paid = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    posted = models.DateTimeField(default=timezone.now)
    contact_email = models.EmailField(blank=True, null=True, help_text='This won\'t be shared with users, rather this is so our team can get in touch with you should we have any issues.')

    def __str__(self):
        return f'{self.title} @ {self.company.name}'
