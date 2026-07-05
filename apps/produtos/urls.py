from django.urls import path
from .views import *

urlpatterns = [
    path("", lista_produtos, name="lista_produtos"),
    path("<slug:slug>detalhes", detalhe_produto, name="detalhe_produto"),
]