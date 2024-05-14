from rest_framework import serializers

from data import models

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset = models.User.objects \
                                              .select_related("userprofile").all())
    event = serializers.PrimaryKeyRelatedField(queryset = models.Event.objects.all())
    parent = serializers.PrimaryKeyRelatedField(queryset = models.Comment.objects.all())
    user_photo = serializers.ImageField(source = "user.userprofile.profile_picture")
    username = serializers.CharField(source = "user.username")
    replies = serializers.PrimaryKeyRelatedField(source = "children", 
                                                 queryset = models.Comment.objects.all(), many = True)

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
            "replies",
        ]
