from rest_framework.viewsets import ModelViewSet
from .models import Ticket
from .serializers import TicketSerializer

class TicketViewSet(ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        return super().get_queryset()
    