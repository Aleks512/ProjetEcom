from rest_framework import serializers
from rest_framework import permissions
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from api.serializers import CustomerSerializer, OrderSerializer
from users.models import Customer, Consultant
from eshop.models import Order, Comment, Product
from contact.models import Message



class CustomerSerializerForConsultant(CustomerSerializer):
    orders = serializers.SerializerMethodField()
    def get_orders(self, customer):
        orders = Order.objects.filter(user=customer, ordered=True)
        return OrderSerializer(orders, many=True).data
    class Meta:
        model = Customer
        fields = ['id', 'user_name', 'email', 'first_name', 'last_name', 'company', 'consultant_applied', 'orders']

class OrderSerializerForConsultant(OrderSerializer):
    ordered = serializers.BooleanField()
    commentaire = serializers.CharField(allow_blank=True)

    class Meta:
        model = Order
        fields = ['ordered', 'commentaire']
        read_only_fields = ['id', 'user', 'quantity', 'ordered_date', 'product']

class ConsultantMessageSerializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField(read_only=True)
    recipient = serializers.SerializerMethodField(read_only=True)
    content = serializers.CharField()

    class Meta:
        model = Message
        fields = ['id', 'sender', 'recipient', 'content', 'timestamp']
        read_only_fields = ['id', 'sender', 'timestamp', 'recipient']

    def get_sender(self, obj):
        return obj.sender.email

    def get_recipient(self, obj):
        return obj.recipient.email




