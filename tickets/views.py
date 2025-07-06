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
        qs = super().get_queryset().select_related('author')

        # For staff
        if self.request.user.is_staff:
            return qs.exclude(status='D')
        
        # For regular users
        return qs.filter(author=self.request.user)

class AdminTicketDetail(generics.RetrieveAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return super().get_queryset().exclude(status='D')