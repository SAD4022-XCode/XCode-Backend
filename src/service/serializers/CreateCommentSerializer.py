from rest_framework import serializers

from data import models

class CreateCommentSerializer(serializers.ModelSerializer):
    parent = serializers.PrimaryKeyRelatedField(queryset = models.Comment.objects.all(), required = False)

    class Meta:
        model = models.Comment
        fields = [
            "text",
            "parent",
        ]

    def create(self, validated_data):
        user_id = self.context.get("user_id")
        event_id = self.context.get("event_id")
        instance = models.Comment.objects.create(user_id = user_id,
                                                 event_id = event_id,
                                                 **validated_data)
        return instance