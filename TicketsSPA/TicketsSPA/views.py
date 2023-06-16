from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic import FormView
from django.contrib.auth.forms import AuthenticationForm


class LoginView(FormView):
    template_name = 'login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            return self.form_invalid(form)
