# Generated by Django 3.1.2 on 2022-04-04 11:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('background', '0007_auto_20220323_1831'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dealership',
            name='dealer1',
        ),
        migrations.RemoveField(
            model_name='dealership',
            name='dealer2',
        ),
    ]
