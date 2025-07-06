from django.db import models
from django.conf import settings

class Ticket(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'D', 'Draft'
        OPEN = 'O', 'Open'
        IN_PROGRESS = 'I', 'In progress'
        CLOSED = 'C', 'Closed'

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tickets',
    )
    title = models.CharField(max_length=255)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=1,
        choices=Status,
        default=Status.DRAFT
    )

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['-created_at'])
        ]

    def __str__(self):
        return f'#{self.id} - {self.title} ({self.status})'