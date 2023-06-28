from django.contrib.admin import AdminSite

class MyAdminSite(AdminSite):
    site_header = "Meu Site de Administração"
    site_title = "Portal de Administração"
    index_title = "Bem-vindo ao Portal de Administração"

admin_site = MyAdminSite(name='my_custom_admin')
