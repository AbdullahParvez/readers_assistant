from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()


class Note(models.Model):
    article = models.ForeignKey('Article', on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(max_length=255)
    content = models.TextField()


class Favourite(models.Model):
    article = models.ForeignKey('Article', on_delete=models.CASCADE, related_name='favourites')
    word = models.CharField(blank=True, null=True, max_length=100)
    meaning = models.CharField(blank=True, null=True, max_length=255)
