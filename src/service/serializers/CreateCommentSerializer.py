from rest_framework import serializers

from data import models

class CreateCommentSerializer(serializers.ModelSerializer):
    event = serializers.PrimaryKeyRelatedField(queryset = models.Event.objects.all())
    parent = serializers.PrimaryKeyRelatedField(queryset = models.Comment.objects.all(), required = False)

    class Meta:
        model = models.Comment
        fields = [
            "event",
            "text",
            "parent",
        ]

    def create(self, validated_data):
        user_id = self.context.get("user_id")
        instance = models.Comment.objects.create(user_id = user_id, **validated_data)
        return instance