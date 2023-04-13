from .views import CustomLoginView, LogoutView, HomePageView
from django.urls import path
from .views import TicketListView, TicketCreateView, TicketUpdateView, TicketDetailView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', TicketListView.as_view(), name='ticket_list'),
    path('create/', TicketCreateView.as_view(), name='ticket_create'),
]
