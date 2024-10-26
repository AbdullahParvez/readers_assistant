from mongoengine import *

class Example(EmbeddedDocument):
    ex_text = StringField(max_length=50)
    ex_sent_jpn = StringField(max_length=250)
    ex_sent_eng = StringField(max_length=250)

class Sense(EmbeddedDocument):
    pos = ListField(StringField(max_length=100))
    meaning = ListField(StringField(max_length=400))
    example = ListField(EmbeddedDocumentField(Example))

class Dictionary_Entry(Document):
    entry = StringField(required=True)
    k_ele = ListField(StringField(max_length=50))
    r_ele = ListField(StringField(max_length=50))
    sense = ListField(EmbeddedDocumentField(Sense))


# from djangotoolbox.fields import ListField, EmbeddedModelField

# # Create your models here.

# class Dictionary_Entry(models.Model):
#     entry = models.CharField()
#     k_ele = ListField(EmbeddedModelField('Kanji_Element'))
#     r_ele = ListField(EmbeddedModelField('Romaji_Element'))
#     sense = EmbeddedModelField('Sense')

# class Kanji_Element(models.Model):
#     keb = models.CharField()
