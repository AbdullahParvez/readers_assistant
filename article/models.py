from django.db import models
from tinymce.models import HTMLField
from django.contrib.auth import get_user_model
user = get_user_model()

class Article(models.Model):
    creator = models.ForeignKey(user, on_delete=models.CASCADE, related_name='articles')
    title = models.CharField(max_length=255)
    content = HTMLField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title


class Note(models.Model):
    article = models.ForeignKey('Article', on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(max_length=255)
    content = HTMLField()

    def __str__(self) -> str:
        return self.title


class Favourite(models.Model):
    article = models.ForeignKey('Article', on_delete=models.CASCADE, related_name='favourites')
    word = models.CharField(blank=True, null=True, max_length=100)
    no = models.CharField(blank=True, null=True, max_length=2)

    def __str__(self) -> str:
        return f"{self.word}_{self.no}"
    
    def get_str(self):
        return self.__str__()

