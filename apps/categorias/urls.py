# apps/categorias/urls.py — CORRETO
from django.urls import path
from . import views

urlpatterns = [
    path('', views.categoria_list, name='categoria_list'),
    path('nova/', views.categoria_create, name='categoria_create'),
    path('<int:pk>/editar/', views.categoria_update, name='categoria_update'),
    path('<int:pk>/excluir/', views.categoria_delete, name='categoria_delete'),
]