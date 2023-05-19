from rest_framework import generics
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from api.serializers import OrderSerializer
from eshop.models import Order


class OrderList(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer