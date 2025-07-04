from rest_framework import serializers
from .models import Ticket

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'title', 'body', 'created_at', 'updated_at', 'status']
        extra_kwargs = {
            'created_at': {'read_only': True}
        }