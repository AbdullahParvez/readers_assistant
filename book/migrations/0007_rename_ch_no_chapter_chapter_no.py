# Generated by Django 4.1.6 on 2023-02-24 10:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0006_alter_chapter_ch_no'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chapter',
            old_name='ch_no',
            new_name='chapter_no',
        ),
    ]
