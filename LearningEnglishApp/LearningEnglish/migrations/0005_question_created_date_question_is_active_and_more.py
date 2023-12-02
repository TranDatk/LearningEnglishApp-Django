# Generated by Django 4.2.7 on 2023-11-24 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LearningEnglish', '0004_rename_fk_titlegrammar_grammar_fk_title_grammar'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='question',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='question',
            name='updated_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]