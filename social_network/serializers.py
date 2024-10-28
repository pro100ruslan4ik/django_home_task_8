from rest_framework import serializers
from social_network import models


class User(serializers.ModelSerializer):
    count_of_messages = serializers.SerializerMethodField()

    def get_count_of_messages(self, obj):
        return models.Message.objects.filter(receiver=obj).count()

    class Meta:
        model = models.User
        fields = '__all__'


class Message(serializers.ModelSerializer):
    sender = User(read_only=True)
    sender_id = serializers.IntegerField(required=False, allow_null=True)
    receiver = User(read_only=True)
    receiver_id = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = models.Message
        fields = '__all__'
