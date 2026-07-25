from django.urls import path
from .views import *
from apps.pedidos.views import comprar_agora

urlpatterns = [
    path("", lista_produtos, name="lista_produtos"),
    path("<int:pk>detalhes", detalhe_produto, name="detalhe_produto"),
    path('variacao/nova/<int:produto_id>/', variacao_create, name='variacao_create'),
    path('variacao/<int:pk>/excluir/', variacao_delete, name='variacao_delete'),
    path('estoque/', estoque_list, name='estoque_list'),
    path('carrinho/adicionar/<int:variacao_id>/', adicionar_ao_carrinho, name='adicionar_ao_carrinho'),
    path('carrinho/', ver_carrinho_cliente, name='ver_carrinho_cliente'),
    path('carrinho/finalizar/', finalizar_compra_cliente, name='finalizar_compra_cliente'),
    path('meus-pedidos/<int:pk>/', meu_pedido_detalhe, name='meu_pedido_detalhe'),
    path('produtos/<slug:slug>/', detalhe_produto_cliente, name='detalhe_produto_cliente'),
    path('produtos/<int:variacao_id>/carrinho/', adicionar_ao_carrinho, name='adicionar_ao_carrinho'),
    path('produtos/<int:variacao_id>/comprar/', comprar_agora, name='comprar_agora'),
]