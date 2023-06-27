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
from django.db.models import F
from django.shortcuts import get_object_or_404, redirect
from .models import Ticket,Comment
from .forms import CommentForm
from django.forms.models import model_to_dict



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
        order_by = self.request.GET.get('order_by')
        if order_by == 'recent':
            threads = TicketThread.objects.order_by(F('updated_at').desc())
        elif order_by == 'oldest':
            threads = TicketThread.objects.order_by('created_at')
        else:
            threads = TicketThread.objects.order_by('-created_at')
        paginator = Paginator(threads, self.paginate_by)

        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['threads'] = page_obj
        context['comment_form'] = CommentForm()
        context['user'] = self.request.user 

        return context


@login_required
def logout_view(request):
    logout(request)
    return redirect('login.html')

from django.http import JsonResponse

@login_required
def add_comment(request, ticket_id):
    data = dict()
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        print(form.is_valid())  # Check if form is valid
        print(form.errors)  # Print form errors
        if form.is_valid():
            comment = form.save(commit=False)
            comment.ticket = ticket
            comment.user = request.user
            comment.save()
            print(comment)
            data['comment'] = model_to_dict(comment) # convert the comment to a dictionary
            data['status'] = 'ok'
            data['comment']['user'] = {
                'username': comment.user.username,
            }
            data['comment']['created_at'] = comment.created_at.strftime('%Y-%m-%d %H:%M:%S')
        else:
            data['status'] = 'error'
    return JsonResponse(data) 


def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST':
        comment.delete()
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'})
