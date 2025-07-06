from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from rest_framework import generics
from .models import Ticket
from .serializers import TicketSerializer

class TicketViewSet(ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        return super().get_queryset()

class AdminTicketDetail(generics.RetrieveAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return super().get_queryset().exclude(status='D')