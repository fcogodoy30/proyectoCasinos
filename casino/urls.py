"""
URL configuration for casino project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from servicio import views
from servicio import ticket

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('principal/', views.principal, name='principal'),
    path('registrar/', views.registrarusuario, name = 'registrar'),
    path('cerrarsession/', views.cerrarsession, name = 'cerrarsession'),
    path('iniciosession/', views.iniciosession, name = 'iniciosession'),
    path('agregarmenu/', views.agregarmenu, name='agregarmenu'),
    path('menu_lista/', views.menu_lista, name='menu_lista'),
    path('principal/programarmenu/', views.programarmenu, name='programarmenu'),
    path('adminCliente/usuarios/', views.usuarios, name = 'usuarios'),
    path('usuarioslistas/', views.usuarioslistas, name='usuarioslistas'),

    path('ticket/<int:usuario_id>/<str:fecha>/', ticket.generar_ticket, name='generar_ticket'),
    
]