from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import serializers
from api.serializers import OrderSerializer, CommentSerializer, MessageSerializer
from contact.models import Message
from eshop.models import Order, Comment
from users.models import Customer, Consultant
from rest_framework.response import Response

from .customer_serializers import OrderSerializerForCustomer, ConsultantSerializerForCustomer
from .serializers import MessageSerializer, CustomerSerializer

# Display the consultant
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_customer_consultant(request):
    customer = request.user.customer
    consultant = customer.consultant_applied

    serializer = ConsultantSerializerForCustomer(consultant)
    return Response(serializer.data)



# Display customer's orders
class OrderListAPIView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    #queryset = Order.objects.all() # tout le monde
    serializer_class = OrderSerializerForCustomer

    def get_queryset(self):
        user = self.request.user.customer  # Récupérer l'utilisateur actuellement authentifié
        if not isinstance(user, Customer):
            raise serializers.ValidationError("Vous n'êtes pas autorisés à acceder à ce jeu de données.")
        return Order.objects.filter(user=user)



# Display customer's order by customer
class OrderDetailAPIView(generics.RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderSerializerForCustomer
    lookup_field = 'id'  # Changer 'id' par le nom du champ utilisé pour la recherche d'une commande spécifique

    def get_queryset(self):
        user = self.request.user  # Récupérer l'utilisateur actuellement authentifié
        return Order.objects.filter(user=user)

class CustomerSendMessageAPIView(generics.CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def perform_create(self, serializer):
        sender = self.request.user.customer
        recipient = sender.consultant_applied
        serializer.save(sender=sender, recipient=recipient)