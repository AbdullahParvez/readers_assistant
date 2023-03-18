from django.db import models
from tinymce.models import HTMLField
from django.contrib.auth import get_user_model
user = get_user_model()

class Book(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE, related_name='books')
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
    chapter = models.ForeignKey('Chapter', on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(max_length=255)
    content = HTMLField()

    def __str__(self) -> str:
        return self.title


class Favourite(models.Model):
    chapter = models.ForeignKey('Chapter', on_delete=models.CASCADE, related_name='favourites')
    word = models.CharField(blank=True, null=True, max_length=100)
    no = models.CharField(blank=True, null=True, max_length=2)

    def __str__(self) -> str:
        return f"{self.word}_{self.no}"
    
    def get_str(self):
        return self.__str__()
