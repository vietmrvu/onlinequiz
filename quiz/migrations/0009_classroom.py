# Generated by Django 4.0.6 on 2023-04-09 04:09

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import froala_editor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0017_remove_teacher_class_model_teacher_class_model'),
        ('student', '0003_student_status'),
        ('quiz', '0008_delete_classmate_alter_docs_name_alter_docs_slug_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Classroom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('subtitle', models.CharField(blank=True, default='', max_length=200)),
                ('class_slug', models.SlugField(unique=True, verbose_name='Class')),
                ('content', froala_editor.fields.FroalaField(blank=True, default='')),
                ('notes', froala_editor.fields.FroalaField(blank=True, default='')),
                ('published', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date published')),
                ('modified', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date modified')),
                ('image', models.ImageField(default='profile_pic/Teacher/no_image.jpg', max_length=255, upload_to='profile_pic/Teacher/')),
                ('author', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='teacher.teacher')),
                ('series', models.ForeignKey(default='', on_delete=django.db.models.deletion.SET_DEFAULT, to='student.student', verbose_name='Series')),
            ],
            options={
                'verbose_name_plural': 'Article',
                'ordering': ['-published'],
            },
        ),
    ]
