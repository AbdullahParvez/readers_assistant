# Generated by Django 4.1.6 on 2024-10-25 04:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0011_article_created_at_article_is_public'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='user',
            new_name='creator',
        ),
    ]
