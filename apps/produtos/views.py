from django.shortcuts import render, get_object_or_404
from .models import Produto


def lista_produtos(request):
    produtos = Produto.objects.filter(ativo=True)
    return render(request, "produtos/lista.html", {"produtos": produtos})

def detalhe_produto(request, slug):
    produto = get_object_or_404(Produto, slug=slug, ativo=True)
    return render(request, "produtos/detalhes.html", {"produto": produto})

def detalhe_produto(request, slug):
    produto = get_object_or_404(Produto, slug=slug, ativo=True)
    variacoes = produto.variacoes.filter(ativo=True)

    return render(request, "produtos/detalhes.html", {
        "produto": produto,
        "variacoes": variacoes
    })