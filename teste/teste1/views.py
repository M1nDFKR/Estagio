from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.views.generic import FormView, RedirectView, TemplateView
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from django.views.generic.edit import FormMixin
from teste1.models import Ticket, Comment


class LoginView(FormView):
    template_name = 'login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            return self.form_invalid(form)


class LogoutView(RedirectView):
    url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)


class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ticket = Ticket.objects.all()  # fetch the first ticket from the database
        context['tickets'] = ticket  # pass the ticket to the template context
        return context

class CustomLoginView(LoginView):
    template_name = 'login.html'
    success_url = reverse_lazy('home')

class TicketDetailView(LoginRequiredMixin, FormMixin, DetailView):
    model = Ticket
    form_class = Comment
    success_url = reverse_lazy('ticket_list')
    template_name = 'ticket.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            comment = form.save(commit=False)
            comment.ticket = self.object
            comment.author = request.user
            comment.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    
