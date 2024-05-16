from rest_framework import serializers

from data import models
from service import serializers as AppSerializers

class CommentListSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset = models.User.objects \
                                              .select_related("userprofile").all())
    event = serializers.PrimaryKeyRelatedField(queryset = models.Event.objects.all())
    parent = serializers.PrimaryKeyRelatedField(queryset = models.Comment.objects.all())
    user_photo = serializers.ImageField(source = "user.userprofile.profile_picture")
    username = serializers.CharField(source = "user.username")
    has_liked = serializers.SerializerMethodField()
    replies = AppSerializers.CommentSerializer(many = True)
    liked_by = serializers.PrimaryKeyRelatedField(queryset = models.User.objects.all(),
                                                  many = True)


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
            "liked_by",
            "has_liked",
            "replies",
        ]

    def get_has_liked(self, instance):
        request_user = self.context.get("request_user")

        if (request_user is not None and instance.liked_by.filter(pk = request_user)):
            return True
        else:
            return False
        

