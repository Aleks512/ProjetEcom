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
    consultant = ConsultantSerializer()
    class Meta:
        model = Customer
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    consultant_name = serializers.CharField(source='consultant.first_name', read_only=True)
    consultant_email = serializers.EmailField(source='consultant.email', read_only=True)
    class Meta:
        model = Comment
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    product = ProductSerializer()  # Champ de sérialiseur imbriqué pour représenter les informations sur le produit
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'sender', 'recipient', 'content', 'timestamp']
        read_only_fields = ['id', 'sender', 'timestamp', 'recipient']


