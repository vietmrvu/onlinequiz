# Generated by Django 4.0.6 on 2022-08-10 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0005_remove_teacher_salary'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='salary',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
