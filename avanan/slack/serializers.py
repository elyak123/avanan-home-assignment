from rest_framework import serializers


class DeleteMessageSerializer(serializers.Serializer):
    timestamp = serializers.FloatField()
    channel = serializers.CharField(max_length=20)
