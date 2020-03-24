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

    @property
    def time_since_posted(self):
        time = timezone.now()
        if self.posted.hour == time.hour:
            delta = str(time.minute - self.posted.minute)
            return delta + f" minute{'s' * (int(delta) != 1)} ago"
        elif self.posted.day == time.day:
            delta = str(time.hour - self.posted.hour)
            return delta + f" hour{'s' * (int(delta) != 1)} ago"
        elif self.posted.month == time.month:
            delta = str(time.day - self.posted.day)
            return delta + f" day{'s' * (int(delta) != 1)} ago"
        elif self.posted.year == time.year:
            delta = str(time.month - self.posted.month)
            return delta + f" month{'s' * (int(delta) != 1)} ago"
        else:
            return 'A while ago'

    def __str__(self):
        return f'{self.title} @ {self.company.name}'
