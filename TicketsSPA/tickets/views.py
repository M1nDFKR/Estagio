from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Ticket
from django.shortcuts import render
from .gmail_mirror import get_emails
from django.core.paginator import Paginator


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
    paginate_by = 5  # Number of tickets per page

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tickets = Ticket.objects.all()
        paginator = Paginator(tickets, self.paginate_by)

        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['tickets'] = page_obj
        context['emails'] = get_emails()
        return context


'''
class HomeView(TemplateView):
    template_name = 'home/home.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tickets'] = Ticket.objects.all()
        context['emails'] = get_emails()
        return context
    
""" for ticket in context['tickets']:
            ticket.relative_image_path = f"tickets/{ticket.}"  # Replace with the correct relative path
        return context """
'''


@login_required
def logout_view(request):
    logout(request)
    return redirect('login.html')

    from django.core.paginator import Paginator
