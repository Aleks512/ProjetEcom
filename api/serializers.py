from rest_framework import serializers
from rest_framework import permissions
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from users.models import Customer, Consultant
from eshop.models import Order, Comment, Product
from contact.models import Message

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        # Ajouter des claims supplémentaires au token JWT si nécessaire
        token = super().get_token(user)
        # token['custom_claim'] = user.custom_claim
        return token


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'image', 'description', 'unit_price', 'stock']

class ConsultantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Consultant
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'user_name', 'email', 'first_name', 'last_name', 'company']


class CommentSerializer(serializers.ModelSerializer):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    consultant_name = serializers.CharField(source='consultant.first_name', read_only=True)
    consultant_email = serializers.EmailField(source='consultant.email', read_only=True)
    class Meta:
        model = Comment
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    user=CustomerSerializer(many=False)
    class Meta:
        model = Order
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    sender_first_name = serializers.ReadOnlyField(source='sender.first_name')
    sender_last_name = serializers.ReadOnlyField(source='sender.last_name')
    sender_email = serializers.ReadOnlyField(source='sender.email')

    recipient_first_name = serializers.ReadOnlyField(source='recipient.first_name')
    recipient_last_name = serializers.ReadOnlyField(source='recipient.last_name')
    recipient_email = serializers.ReadOnlyField(source='recipient.email')

    class Meta:
        model = Message
        fields = ['id', 'sender', 'recipient', 'content', 'timestamp',
                  'sender_first_name', 'sender_last_name', 'sender_email',
                  'recipient_first_name', 'recipient_last_name', 'recipient_email']
        read_only_fields = ['id', 'sender', 'timestamp', 'recipient',
                            'sender_first_name', 'sender_last_name', 'sender_email',
                            'recipient_first_name', 'recipient_last_name', 'recipient_email']



