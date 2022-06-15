from django.conf import settings
from rest_framework import serializers
from .models import Tweet

MAX_ZWEET_LENGTH = settings.MAX_ZWEET_LENGTH

class TweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tweet
        fields = ['content']

    def validate_content(self, value):
        if len(value) > MAX_ZWEET_LENGTH:
            raise serializers.ValidationError("The tweet is too long")
        return value

