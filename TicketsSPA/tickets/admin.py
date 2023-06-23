from django.contrib import admin
from .models import Ticket, TicketThread

admin.site.register(Ticket)
admin.site.register(TicketThread)
