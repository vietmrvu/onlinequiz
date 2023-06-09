# Generated by Django 4.0.6 on 2022-10-01 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0007_alter_teacher_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='class_model',
            field=models.IntegerField(choices=[(0, 'Computer'), (1, 'Gears for PC'), (2, 'Tutorial'), (3, 'Vehicle')], default=3),
        ),
        migrations.AddField(
            model_name='teacher',
            name='grade',
            field=models.IntegerField(choices=[(0, '6'), (1, '7'), (2, '8'), (3, '9')], default=0),
        ),
    ]
