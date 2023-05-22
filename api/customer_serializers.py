from rest_framework import serializers
from rest_framework import permissions
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from api.serializers import CustomerSerializer, ConsultantSerializer, OrderSerializer, ProductSerializer, CommentSerializer
from users.models import Customer, Consultant
from eshop.models import Order, Comment, Product
from contact.models import Message

class CustomerSerializerForCustomer(CustomerSerializer):
    consultant = ConsultantSerializer()
    class Meta:
        model = Customer
        fields = '__all__'
class OrderSerializerForCustomer(OrderSerializer):
    product = ProductSerializer()  # Champ de sérialiseur imbriqué pour représenter les informations sur le produit
    comments = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields ='__all__'

class ConsultantSerializerForCustomer(ConsultantSerializer):
    class Meta:
        model = Consultant
        fields = ['id', 'matricule', 'email', 'first_name', 'last_name',]




