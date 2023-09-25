from django.db import models

# Create your models here.

class JLPT(models.Model):
    level = models.CharField(max_length=5)

    def __str__(self) -> str:
        return self.level

class Unit(models.Model):
    level = models.ForeignKey(JLPT, on_delete=models.CASCADE, related_name='units')
    no = models.IntegerField()

    def __str__(self) -> str:
        return f'{self.level}\'s unit {self.no}'
    

class Vocab(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='vocabs')
    pronunciation = models.CharField(max_length=20)
    word = models.CharField(max_length=20)
    meaning = models.CharField(max_length=500)
