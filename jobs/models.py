from django.db import models
from django.utils import timezone


class Company(models.Model):
    name = models.CharField(max_length=128)
    location = models.CharField(max_length=64)
    url = models.URLField()
    logo = models.ImageField(blank=True)

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
    name = models.CharField(max_length=64)
    color = models.CharField(max_length=32, default='dark')

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Job(models.Model):
    title = models.CharField(max_length=128)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    hours_per_week = models.IntegerField()
    application_link = models.URLField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    description = models.TextField()
    qualifications = models.TextField()
    posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.title} @ {self.company.name}'
