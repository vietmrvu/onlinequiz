# Generated by Django 4.0.6 on 2022-10-13 04:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0005_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='active',
        ),
    ]