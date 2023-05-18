from rest_framework import serializers
from users.models import Customer, Consultant
from contact.models import Message

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'