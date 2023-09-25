from rest_framework import serializers


class KanjiSerializer(serializers.Serializer):
    '''Serializer for kanji details.'''
    details = serializers.CharField(max_length=5000)
