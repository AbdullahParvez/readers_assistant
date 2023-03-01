from django.db import models
from tinymce.models import HTMLField


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self) -> str:
        return self.title


class Chapter(models.Model):
    book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='chapters')
    title = models.CharField(max_length=255)
    chapter_no = models.CharField(max_length=10)
    content = HTMLField()


class Note(models.Model):
    book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(max_length=255)
    content = models.TextField()


class Favourite(models.Model):
    book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='favourites')
    word = models.CharField(blank=True, null=True, max_length=100)
    meaning = models.CharField(blank=True, null=True, max_length=255)
