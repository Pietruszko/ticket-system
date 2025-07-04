from rest_framework import serializers
from .models import Ticket

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'title', 'body', 'created_at', 'updated_at', 'status']
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True}
        }

    def validate_status(self, value):
        # Prevent invalid transitions (draft to closed or in progress)
        if self.instance and self.instance.status == 'D':
            if value in ['I', 'C']:
                raise serializers.ValidationError('Cannot close ticket that is in draft.')
            
        return value

    def validate(self, data):
        # Prevent changing status for closed tickets
        if self.instance and self.instance.status == 'C':
            raise serializers.ValidationError('Cannot change status of a closed ticket.')
        
        # Prevent creating tickets as closed or in progress
        if not self.instance:
            if data.get('status') in ['I', 'C']:
                raise serializers.ValidationError('Cannot create tickets as closed or in progress')
            
        return data
    
    # def create(self, validated_data):
        # Assign user on creating ticket