# Generated by Django 4.2.7 on 2023-11-24 09:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LearningEnglish', '0003_titlegrammar_alter_question_correct_answer_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='grammar',
            old_name='fk_titlegrammar',
            new_name='fk_title_grammar',
        ),
    ]
