from rest_framework import serializers


class VocabSerializer(serializers.Serializer):
    '''Serializer for vocab details.'''
    details = serializers.CharField(max_length=5000)
