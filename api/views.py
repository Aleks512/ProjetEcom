from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from api.serializers import OrderSerializer
from eshop.models import Order


# class OrderList(generics.ListCreateAPIView):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer

class OrderListAPIView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    #queryset = Order.objects.all() # tout le monde
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user  # Récupérer l'utilisateur actuellement authentifié
        return Order.objects.filter(user=user)  # Filtrer les commandes pour l'utilisateur actuel

class OrderDetailAPIView(generics.RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = 'id'  # Changer 'id' par le nom du champ utilisé pour la recherche d'une commande spécifique

    def get_queryset(self):
        user = self.request.user  # Récupérer l'utilisateur actuellement authentifié
        return Order.objects.filter(user=user)