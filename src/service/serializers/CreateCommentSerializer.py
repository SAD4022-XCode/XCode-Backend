from rest_framework import serializers

from data import models

class CreateCommentSerializer(serializers.ModelSerializer):
    event = serializers.PrimaryKeyRelatedField(queryset = models.Event.objects.all())

    class Meta:
        model = models.Comment
        fields = [
            "event",
            "text",
        ]

    def create(self, validated_data):
        user_id = self.context.get("user_id")
        parent_id = self.context.get("parent_id")
        instance = models.Comment.objects.create(user_id = user_id, 
                                                 parent_id = parent_id, 
                                                 **validated_data)
        return instance