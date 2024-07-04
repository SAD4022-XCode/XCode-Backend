from rest_framework import serializers

class AnalyticsSerializer(serializers.Serializer):
    registered_users = serializers.IntegerField()
    free_inperson_events = serializers.IntegerField()
    paid_inperson_events = serializers.IntegerField()
    free_online_events = serializers.IntegerField()
    paid_online_events = serializers.IntegerField()