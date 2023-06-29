from django.urls import path
from django.contrib.auth import views as auth_views
from TicketsSPA.myadmin import admin_site
from . import views

urlpatterns = [
    path('', auth_views.LoginView.as_view(
        template_name='login.html'), name='login'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('home/', views.HomeView.as_view(template_name='home.html'), name='home'),
    path('myadmin/', admin_site.urls),
    path('add_comment/<int:ticket_id>/', views.add_comment, name='add_comment'),
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('logout_on_close/', views.logout_on_close, name='logout_on_close'),
]
