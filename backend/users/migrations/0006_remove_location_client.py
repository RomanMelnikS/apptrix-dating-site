# Generated by Django 3.2.9 on 2021-11-28 11:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20211128_1613'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='location',
            name='client',
        ),
    ]
