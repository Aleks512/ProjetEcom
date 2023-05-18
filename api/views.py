from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from users.models import Customer, Consultant
from contact.models import Message
from .serializers import MessageSerializer

@api_view(['GET'])
def getData(request):
    messages = Message.objects.all()
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data)

@api_view(['POST'])  # Ajout de la méthode POST
def addData(request):
    serializer = MessageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


class MessageList(APIView):
    def get(self, request):
        messages = Message.objects.all()[:20]
        data = MessageSerializer(messages, many=True).data
        return Response(data)

class MessageDetail(APIView):
    def get(self, request, pk):
        message = get_object_or_404(Message, pk=pk)
        data = MessageSerializer(message).data
        return Response(data)

# class MessageList(generics.ListCreateAPIView):
#     queryset = Message.objects.all()
#     serializer_class = MessageSerializer
# class MessageDetail(generics.RetrieveDestroyAPIView):
#     queryset = Message.objects.all()
#     serializer_class = MessageSerializer