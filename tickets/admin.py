from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Ticket

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'status', 'ticket_detail_link','created_at', 'updated_at']
    list_filter = ['status', 'created_at', 'updated_at', 'author']
    search_fields = ['title', 'body']
    ordering = ['created_at', 'status']

    def ticket_detail_link(self, obj):
        url = reverse('admin-ticket-detail', args=[obj.id])
        return format_html('<a href="{}">View Ticket</a>', url)
