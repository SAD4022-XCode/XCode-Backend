from rest_framework import serializers

class DepositSerializer(serializers.Serializer):
    amount = serializers.IntegerField()