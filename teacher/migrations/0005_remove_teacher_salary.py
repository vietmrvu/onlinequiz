# Generated by Django 4.0.6 on 2022-08-10 12:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0004_alter_teacher_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teacher',
            name='salary',
        ),
    ]
