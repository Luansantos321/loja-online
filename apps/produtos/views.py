from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.core.exceptions import ValidationError
from .services import registrar_saida, registrar_entrada
from .models import Produto, VariacaoProduto, MovimentacaoEstoque
from django.contrib.auth.decorators import login_required
from apps.pedidos.cart import Carrinho
from django.db import transaction
from apps.pedidos.models import Pedido, ItemPedido
from .services import registrar_saida
from django.contrib.auth.decorators import login_required




def lista_produtos(request):
    produtos = Produto.objects.filter(ativo=True)
    return render(request, "painel/produtos/lista.html", {"produtos": produtos})

def detalhe_produto_cliente(request, slug):
    produto = get_object_or_404(
        Produto.objects.select_related("categoria"),
        slug=slug,
        ativo=True
    )
    variacoes = produto.variacoes.all()
    imagens = produto.imagens.all()

    return render(
        request,
        "produtos/detalhes.html",
        {
            "produto": produto,
            "variacoes": variacoes,
            "imagens": imagens,
        },
    )

def detalhe_produto(request, pk):
    produto = get_object_or_404(
        Produto.objects.select_related("categoria"),
        pk=pk,
        ativo=True
    )
    variacoes = produto.variacoes.all()
    imagens = produto.imagens.all()

    return render(
        request,
        "painel/produtos/detalhes.html",
        {
            "produto": produto,
            "variacoes": variacoes,
            "imagens": imagens,
        },
    )


def variacao_create(request, produto_id):
    produto = get_object_or_404(Produto, pk=produto_id)

    if request.method == 'POST':
        tamanho = request.POST.get('tamanho', '').strip()
        cor = request.POST.get('cor', '').strip()
        sku = request.POST.get('sku', '').strip()
        preco = request.POST.get('preco', '0').replace(',', '.')
        quantidade_inicial = int(request.POST.get('quantidade_inicial', 0))
        imagem = request.FILES.get('imagem')

        try:
            variacao = VariacaoProduto.objects.create(
                produto=produto,
                tamanho=tamanho,
                cor=cor,
                sku=sku,
                preco=preco,
                imagem=imagem,
            )
            if quantidade_inicial > 0:
                registrar_entrada(
                    variacao_id=variacao.pk,
                    quantidade=quantidade_inicial,
                    motivo='Estoque inicial',
                    usuario=request.user if request.user.is_authenticated else None,
                )
            messages.success(request, 'Variação cadastrada com sucesso!')
        except ValidationError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, f'Erro ao cadastrar variação: {e}')

        return redirect('detalhe_produto', produto.pk)

    return render(request, 'painel/produtos/variacao_form.html', {'produto': produto})


def variacao_delete(request, pk):
    variacao = get_object_or_404(VariacaoProduto, pk=pk)
    produto_id = variacao.produto_id

    if request.method == "POST":
        MovimentacaoEstoque.objects.filter(variacao=variacao).delete()
        variacao.delete()

        messages.success(request, "Variação removida com sucesso.")
        return redirect("detalhe_produto", produto_id)

    return render(
        request,
        "painel/produtos/variacao_confirm_delete.html",
        {"variacao": variacao},
    )

def vender_produto(request, variacao_id):
    if request.method == 'POST':
        quantidade = int(request.POST.get('quantidade', 0))
        try:
            registrar_saida(
                variacao_id=variacao_id,
                quantidade=quantidade,
                motivo='Venda balcão',
                usuario=request.user if request.user.is_authenticated else None,
            )
            messages.success(request, 'Venda registrada e estoque atualizado!')
        except ValidationError as e:
            messages.error(request, str(e))

        return redirect('estoque_list')

def estoque_list(request):
    variacoes = VariacaoProduto.objects.select_related('produto').order_by('produto__nome')

    busca = request.GET.get('busca')
    if busca:
        variacoes = variacoes.filter(produto__nome__icontains=busca)

    return render(request, 'painel/produtos/estoque_list.html', {
        'variacoes': variacoes,
    })

@login_required
def adicionar_ao_carrinho(request, variacao_id):
    carrinho = Carrinho(request)
    quantidade = int(request.POST.get('quantidade', 1))
    carrinho.adicionar(variacao_id, quantidade)
    messages.success(request, 'Produto adicionado ao carrinho!')
    return redirect('ver_carrinho_cliente')


@login_required
def ver_carrinho_cliente(request):
    carrinho = Carrinho(request)
    return render(request, 'carrinho/carrinho_cliente.html', {'carrinho': carrinho})


@login_required
def finalizar_compra_cliente(request):
    carrinho = Carrinho(request)

    if len(carrinho) == 0:
        messages.error(request, 'Seu carrinho está vazio.')
        return redirect('ver_carrinho_cliente')

    try:
        with transaction.atomic():
            pedido = Pedido.objects.create(
                cliente=request.user,
                atendente=None,
                status=Pedido.FINALIZADO,
            )

            for item in carrinho:
                ItemPedido.objects.create(
                    pedido=pedido,
                    variacao=item['variacao'],
                    quantidade=item['quantidade'],
                    preco_unitario=item['preco'],
                )
                registrar_saida(
                    variacao_id=item['variacao'].pk,
                    quantidade=item['quantidade'],
                    motivo=f'Venda site - Pedido #{pedido.pk}',
                    usuario=request.user,
                )

        carrinho.limpar()
        messages.success(request, f'Compra finalizada! Pedido #{pedido.pk}.')
        return redirect('meu_pedido_detalhe', pk=pedido.pk)

    except ValidationError as e:
        messages.error(request, str(e))
        return redirect('ver_carrinho_cliente')


@login_required
def meu_pedido_detalhe(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk, cliente=request.user)
    return render(request, 'painel/produtos/meu_pedido_detalhe.html', {'pedido': pedido})