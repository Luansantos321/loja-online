from django.urls import path
from . import views

urlpatterns = [
    path('carrinho/', views.carrinho_ver, name='carrinho_ver'),
    path('carrinho/adicionar/<int:variacao_id>/', views.carrinho_adicionar, name='carrinho_adicionar'),
    path('carrinho/remover/<int:variacao_id>/', views.carrinho_remover, name='carrinho_remover'),
    path('carrinho/finalizar/', views.finalizar_pedido, name='finalizar_pedido'),
    path('', views.pedido_list, name='pedido_list'),
    path('<int:pk>/', views.pedido_confirmado, name='pedido_confirmado'),
]