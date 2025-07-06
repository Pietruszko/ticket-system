from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Ticket

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']
        read_only_fields = ['first_name', 'last_name']

class TicketSerializer(serializers.ModelSerializer):
    # Show author for staff users
    author = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = ['id', 'author', 'title', 'body', 'status', 'created_at', 'updated_at']
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True}
        }

    def get_author(self, obj):
        """Custom method for author field control."""
        request = self.context.get('request')
        if request and request.user.is_staff:
            return UserSerializer(obj.author).data
        return None

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
    
    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')

        if not request.user.is_staff:
            # Regular user sees minimal data
            return {
                'title': data['title'],
                'body': data['body'],
                'status': data['status'],
                'created_at': data['created_at'],
                'updated_at': data['updated_at']
            }
        else:
            # Admins see all needed fields
            data.pop('id', None)
            data.pop('email', None)
            return data