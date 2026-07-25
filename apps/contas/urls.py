from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('clientes/', views.cliente_list, name='cliente_list'),
    path('clientes/<int:pk>/', views.cliente_detalhe, name='cliente_detalhe'),
    path('login/', auth_views.LoginView.as_view(template_name='contas/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('cadastro/', views.cadastro_cliente, name='cadastro_cliente'),
]