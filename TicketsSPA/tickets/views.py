from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Ticket, TicketThread
from .gmail_mirror import get_emails
from .gmail_mirror import create_ticket_instances
from django.core.paginator import Paginator
from django.shortcuts import render
from .forms import TicketFilterForm


class LoginView(TemplateView):
    template_name = 'login.html'

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, self.template_name)


class HomeView(TemplateView):
    template_name = 'home/home.html'
    paginate_by = 10  # Number of tickets per page

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        emails = get_emails()
        create_ticket_instances(emails)
        tickets = Ticket.objects.all()
        threads = TicketThread.objects.all()
        paginator = Paginator(threads, self.paginate_by)

        emails = get_emails()
        create_ticket_instances(emails)
        tickets = Ticket.objects.all()

        form = TicketFilterForm(self.request.GET)

        if form.is_valid():

            if form.cleaned_data['title']:
                tickets = tickets.filter(
                    title__icontains=form.cleaned_data['title'])
            if form.cleaned_data['status'] and form.cleaned_data['status'] != "":
                tickets = tickets.filter(status=form.cleaned_data['status'])

        paginator = Paginator(tickets, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['form'] = form
        context['tickets'] = page_obj
        context['emails'] = Email.objects.all()
        context['threads'] = page_obj

        return context


@login_required
def logout_view(request):
    logout(request)
    return redirect('login.html')
