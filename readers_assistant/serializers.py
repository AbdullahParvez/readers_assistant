from rest_framework import serializers
from jmdict.models import Dictionary_Entry, Sense, Example
from rest_framework_mongoengine.serializers import DocumentSerializer, EmbeddedDocumentSerializer

class ExampleSerializer(EmbeddedDocumentSerializer):
    class Meta:
        model = Example
        depth = 2
        fields = ('ex_sent_jpn', 'ex_sent_eng')


class SenseSerializer(EmbeddedDocumentSerializer):
    class Meta:
        model = Sense
        depth = 2
        fields = ('pos', 'meaning', 'example')


class VocabSerializer(DocumentSerializer):
    class Meta:
        model = Dictionary_Entry
        depth = 2
        fields = ('k_ele', 'r_ele', 'sense')

# class VocabSerializer(serializers.Serializer):
#     '''Serializer for vocab details.'''
#     details = serializers.CharField(max_length=5000)
