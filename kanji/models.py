from django.db import models


class Radical(models.Model):
    radical = models.CharField(max_length=2)
    radical_number = models.IntegerField()
    number_of_stroke = models.IntegerField()
    alternative = models.CharField(max_length=20)
    meaning = models.CharField(max_length=50)
    readings = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.radical}'


class Kanji (models.Model):
    kanji = models.CharField(max_length=2)
    onyomi = models.CharField(max_length=50)
    kunyomi = models.CharField(max_length=100)
    meaning = models.CharField(max_length=200)
    examples = models.CharField(max_length=7000)
    jlpt_level = models.CharField(max_length=2)
    no_of_strokes = models.IntegerField()
    radical = models.ForeignKey(Radical, on_delete=models.CASCADE, null=True, blank=True)
    parts = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f'{self.kanji}'
