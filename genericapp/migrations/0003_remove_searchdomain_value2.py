# Generated by Django 4.2.8 on 2023-12-30 14:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('genericapp', '0002_searchdomain_value2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='searchdomain',
            name='value2',
        ),
    ]