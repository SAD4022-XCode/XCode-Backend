from rest_framework import serializers

class AnalyticsSerializer(serializers.Serializer):
    free_events = serializers.IntegerField()
    paid_events = serializers.IntegerField()
    in_person_events = serializers.IntegerField()
    online_events = serializers.IntegerField()