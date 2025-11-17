from rest_framework import serializers
from .models import ShortenedURL


class ShortURLCreateSerializer(serializers.ModelSerializer):
    original_url = serializers.URLField(max_length=2048)

    class Meta:
        model = ShortenedURL
        fields = ["original_url"]


class ShortURLSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortenedURL
        fields = "__all__"
