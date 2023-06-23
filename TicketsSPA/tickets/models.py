from django.db import models
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey
import re
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Ticket(MPTTModel):
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
    level = models.IntegerField(default=0)
    lft = models.IntegerField(default=0)
    rght = models.IntegerField(default=0)
    tree_id = models.IntegerField(default=0)
    parent = TreeForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True, related_name='next_ticket')

    all_tickets = models.Manager()

    class MPTTMeta:
        order_insertion_by = ['created_at']

    def associate_code_from_email(self, code):
        self.code = code
        self.save()

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
