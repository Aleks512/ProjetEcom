from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import serializers
from api.serializers import OrderSerializer, CommentSerializer, MessageSerializer
from contact.models import Message
from eshop.models import Order, Comment
from users.models import Customer, Consultant
from rest_framework.response import Response

from .consultant_serializers import CustomerSerializerForConsultant, OrderSerializerForConsultant, \
    ConsultantMessageSerializer
from .serializers import MessageSerializer, CustomerSerializer


class ClientListAPIView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Customer.objects.all() # tout le monde
    serializer_class = CustomerSerializerForConsultant

    def get_queryset(self):
        user = self.request.user.consultant  # Récupérer l'utilisateur actuellement authentifié
        if not isinstance(user, Consultant):
            raise serializers.ValidationError("Vous n'êtes pas autorisés à acceder à ce jeu de données. Vous n'êtes pas un consultant.")
        return Customer.objects.filter(consultant_applied=user)  # Filtrer les commandes pour l'utilisateur actuel



# Display customer's order by customer
class ClientDetailAPIView(generics.RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializerForConsultant
    lookup_field = 'id'  # Changer 'id' par le nom du champ utilisé pour la recherche d'un client spécifique

    def get_queryset(self):
        user = self.request.user.consultant  # Récupérer l'utilisateur actuellement authentifié
        if not isinstance(user, Consultant):
            raise serializers.ValidationError("Vous n'êtes pas autorisés à acceder à ce jeu de données. Vous n'êtes pas un consultant.")
        return Customer.objects.filter(consultant_applied=user).prefetch_related('orders')




@api_view(['PUT'])
def consultant_order_update_status(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return Response({'error': 'Commande de commande trouvée'}, status=status.HTTP_404_NOT_FOUND)

    if order.user.consultant_applied != request.user.consultant:
        return Response({'error': "Vous n'êtes pas autorisés à acceder à ce jeu de données."}, status=status.HTTP_403_FORBIDDEN)

    order.ordered = False  # Mise à jour du statut
    order.commentaire = request.data.get('commentaire', '')  # Récupération du commentaire depuis la requête
    order.save()

    return Response(OrderSerializerForConsultant(order).data)

class ConsultantSendMessageAPIView(generics.CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def perform_create(self, serializer):
        sender = self.request.user.consultant
        recipient = sender.clients
        serializer.save(sender=sender, recipient=recipient)


class ConsultantSendMessageAPIView(generics.CreateAPIView):
    serializer_class = ConsultantMessageSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def perform_create(self, serializer):
        user = self.request.user.consultant

        if not hasattr(user, 'consultant'):
            raise PermissionDenied('Only consultants are allowed to send messages.')

        sender = user.consultant
        recipient_id = self.kwargs['recipient_id']
        recipient = Customer.objects.get(id=recipient_id)

        serializer.save(sender=sender, recipient=recipient)


