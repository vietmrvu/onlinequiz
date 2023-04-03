# Generated by Django 4.0.6 on 2022-11-05 08:44

from django.db import migrations, models
import froala_editor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0006_remove_comment_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='Classmate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default=True, max_length=100)),
                ('content', froala_editor.fields.FroalaField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
