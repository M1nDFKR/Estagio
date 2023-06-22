from django.db import models
from django.contrib.auth.models import User
import re

class Ticket(models.Model):
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    STATUS_CHOICES = (
        ('A', 'Aberto'),
        ('F', 'Fechado'),
    )
    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, default='A')
    code = models.CharField(max_length=14)
    files = models.FileField(upload_to='static/uploads',
                             blank=True)
    responses = models.TextField(blank=True)
    subject_from_email = models.TextField(blank=True)

    def associate_code_from_email(self, code):
        self.code = code
        self.save()

    def __str__(self):
        return self.title


class Email(models.Model):
    assunto = models.CharField(max_length=255)
    corpo = models.TextField()
    ticket = models.ForeignKey(
        Ticket, default=None, on_delete=models.CASCADE, related_name='emails')

    def __str__(self):
        return self.assunto


class Comment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.ticket.title} - {self.user.username}"
