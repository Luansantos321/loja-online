from django.urls import path

from . import views

urlpatterns = [

    path("",views.dashboard,name="painel_dashboard"),
    path("produtos/",views.produtos_lista,name="painel_produtos"),
    path("produtos/novo/",views.produto_novo,name="painel_produto_novo"),
    path("produtos/<int:pk>/",views.produto_detalhe,name="painel_produto_detalhe"),
    path("produtos/<int:pk>/editar/", views.produto_editar,name="painel_produto_editar"),
    path( "produtos/<int:pk>/excluir/", views.produto_excluir, name="painel_produto_excluir"),
    path('<int:pk>/excluir-definitivo/', views.produto_excluir_definitivo, name='painel_produto_excluir_definitivo'),
    path("marcas/",views.marcas_lista,name="painel_marcas"),
    path("marcas/nova/",views.marca_nova,name="painel_marca_nova"),
    path("marcas/<int:pk>/editar/",views.marca_editar,name="painel_marca_editar"),
    path("marcas/<int:pk>/excluir/", views.marca_excluir,name="painel_marca_excluir"),

]