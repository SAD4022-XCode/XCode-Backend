from rest_framework import serializers

from data.models import Tag

class TagSerializer(serializers.ModelSerializer):
    tag = serializers.CharField(max_length = 255, required = False)

    class Meta:
        model = Tag
        fields = [
            'tag',
        ]