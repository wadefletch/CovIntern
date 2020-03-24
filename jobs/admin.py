from django.contrib import admin

from .models import Category, Company, Job

admin.site.register(Job)
admin.site.register(Category)
admin.site.register(Company)
