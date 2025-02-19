# Generated by Django 4.1.6 on 2023-02-24 10:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0003_favourite_remove_chapter_book_alter_note_title_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favourite',
            name='article',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favourites', to='article.article'),
        ),
        migrations.AlterField(
            model_name='note',
            name='article',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='articles', to='article.article'),
        ),
    ]
