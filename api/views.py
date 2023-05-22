from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import serializers
from api.serializers import OrderSerializer, CommentSerializer, MessageSerializer
from contact.models import Message
from eshop.models import Order, Comment
from users.models import Customer, Consultant
from rest_framework.response import Response
from .serializers import MessageSerializer, CustomerSerializer

class OrderList(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class CommentListAPIView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class CommentDetailAPIView(generics.RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = 'id'  # Changer 'id' par le nom du champ utilisé pour la recherche d'un commentaire spécifique


class CommentCreateAPIView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        order_id = self.request.data.get('order_id')
        order = Order.objects.get(id=order_id)
        serializer.save(consultant=self.request.user, order=order)

class MessageCreateAPIView(generics.CreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        recipient_id = self.request.data.get('recipient_id')
        recipient = Order.objects.get(id=recipient_id).user
        serializer.save(sender=self.request.user, recipient=recipient)

