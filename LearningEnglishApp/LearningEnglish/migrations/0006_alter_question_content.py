# Generated by Django 4.2.7 on 2023-11-29 04:12

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LearningEnglish', '0005_question_created_date_question_is_active_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='content',
            field=ckeditor.fields.RichTextField(blank=True),
        ),
    ]
