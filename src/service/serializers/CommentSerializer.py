from rest_framework import serializers

from data import models

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset = models.User.objects \
                                              .select_related("userprofile").all())
    event = serializers.PrimaryKeyRelatedField(queryset = models.Event.objects.all())
    parent = serializers.PrimaryKeyRelatedField(queryset = models.Comment.objects.all())
    user_photo = serializers.ImageField(source = "user.userprofile.profile_picture")
    username = serializers.CharField(source = "user.username")

    class Meta:
        model = models.Comment

        fields = [
            "id",
            "user",
            "event",
            "parent",
            "user_photo",
            "username",
            "created_at",
            "score",
            "text",
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        serializer = CommentSerializer(instance.children.prefetch_related("children").all(), many = True)
        representation["replies"] = serializer.data
        return representation
