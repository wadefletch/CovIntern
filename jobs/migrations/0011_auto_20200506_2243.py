# Generated by Django 2.1.15 on 2020-05-06 22:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0010_auto_20200506_0756'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='logo',
            field=models.ImageField(default='/static/images/default_logo.png', upload_to=''),
        ),
    ]
