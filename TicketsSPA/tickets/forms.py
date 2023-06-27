from django import forms
from .models import Ticket, Comment
from django.contrib.auth.forms import UserCreationForm


class TicketFilterForm(forms.ModelForm):
    STATUS_CHOICES = [
        ("", "Todos"),
        ("A", "Aberto"),
        ("F", "Fechado"),
    ]

    status = forms.ChoiceField(choices=STATUS_CHOICES)

    class Meta:
        model = Ticket
        fields = [ 'title', 'status']

    def __init__(self, *args, **kwargs):
        super(TicketFilterForm, self).__init__(*args, **kwargs)
        self.fields['title'].required = False
        self.fields['status'].required = False

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
