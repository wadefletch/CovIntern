from django.contrib import admin

from .models import Category, Company, Job


class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'category', 'posted', 'application_deadline')


admin.site.register(Job, JobAdmin)
admin.site.register(Category)
admin.site.register(Company)
