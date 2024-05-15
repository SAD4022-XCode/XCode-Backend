from rest_framework import serializers

from data import models

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset = models.User.objects \
                                              .select_related("userprofile").all())
    event = serializers.PrimaryKeyRelatedField(queryset = models.Event.objects.all())
    parent = serializers.PrimaryKeyRelatedField(queryset = models.Comment.objects.all())
    user_photo = serializers.ImageField(source = "user.userprofile.profile_picture")
    username = serializers.CharField(source = "user.username")
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
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request_user = self.context.get("request_user")

        if (request_user is not None and instance.liked_by.filter(pk = request_user)):
            representation["has_liked"] = True
        else:
            representation["has_liked"] = False
        
        serializer = CommentSerializer(instance.children \
                                        .prefetch_related("children", "liked_by") \
                                        .select_related("user", "event") \
                                        .all(), 
                                       many = True, 
                                       context = self.context)
        representation["replies"] = serializer.data
        
        return representation
