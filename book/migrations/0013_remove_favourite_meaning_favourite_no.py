# Generated by Django 4.1.6 on 2023-03-18 05:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0012_alter_note_content'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='favourite',
            name='meaning',
        ),
        migrations.AddField(
            model_name='favourite',
            name='no',
            field=models.CharField(blank=True, max_length=2, null=True),
        ),
    ]
