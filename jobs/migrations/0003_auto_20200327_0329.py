# Generated by Django 2.1.15 on 2020-03-27 03:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0002_auto_20200327_0323'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='notes',
        ),
        migrations.AlterField(
            model_name='job',
            name='contact_email',
            field=models.EmailField(help_text="This won't be shared with users, rather this is so our team can get in touch with you should we have any issues.", max_length=254),
        ),
    ]
