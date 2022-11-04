# Generated by Django 4.0.6 on 2022-11-04 10:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0016_delete_scratch'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teacher',
            name='class_model',
        ),
        migrations.AddField(
            model_name='teacher',
            name='class_model',
            field=models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, to='teacher.tag'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='profile_pic',
            field=models.ImageField(blank=True, default='image/teacher.png', null=True, upload_to='profile_pic/Teacher/'),
        ),
    ]
