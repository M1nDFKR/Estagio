from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from TicketsSPA.myadmin import admin_site




urlpatterns = [
    path('', auth_views.LoginView.as_view(
        template_name='login.html'), name='login'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('home/', views.HomeView.as_view(template_name='home.html'), name='home'),
    path('myadmin/', admin_site.urls),
]
