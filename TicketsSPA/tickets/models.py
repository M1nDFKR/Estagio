from django.db import models
from django.contrib.auth.models import User


class Ticket(models.Model):
    title = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    STATUS_CHOICES = (
        ('A', 'Aberto'),
        ('F', 'Fechado'),
    )
    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, default='A')

    def __str__(self):
        return self.title


class Comment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.ticket.title} - {self.user.username}"
