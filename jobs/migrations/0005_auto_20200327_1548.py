# Generated by Django 2.1.15 on 2020-03-27 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0004_auto_20200327_0352'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='hours_per_week',
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=64, verbose_name='Company Name'),
        ),
        migrations.AlterField(
            model_name='company',
            name='url',
            field=models.URLField(help_text="This should be the url of your company's homepage, not your job posting or application."),
        ),
    ]