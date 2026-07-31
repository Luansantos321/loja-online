from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required
from django.core.exceptions import ValidationError
from django.db import transaction
from apps.produtos.models import VariacaoProduto
from apps.produtos.services import registrar_saida
from .cart import Carrinho
from .models import Pedido, ItemPedido 
from apps.contas.models import Usuario



def eh_funcionario(user):
    return user.is_authenticated and user.is_staff


@user_passes_test(eh_funcionario, login_url='login')
def carrinho_adicionar(request, variacao_id):
    carrinho = Carrinho(request)
    quantidade = int(request.POST.get('quantidade', 1))
    carrinho.adicionar(variacao_id, quantidade)
    messages.success(request, 'Item adicionado ao carrinho.')
    return redirect('carrinho_ver')


@user_passes_test(eh_funcionario, login_url='login')
def carrinho_remover(request, variacao_id):
    carrinho = Carrinho(request)
    carrinho.remover(variacao_id)
    return redirect('carrinho_ver')



@user_passes_test(eh_funcionario, login_url='login')
def carrinho_ver(request):
    carrinho = Carrinho(request)
    clientes = Usuario.objects.filter(is_staff=False).order_by('first_name')
    return render(request, 'painel/pedidos/carrinho.html', {
        'carrinho': carrinho,
        'clientes': clientes,
    })

@user_passes_test(eh_funcionario, login_url='login')
def finalizar_pedido(request):
    carrinho = Carrinho(request)

    if len(carrinho) == 0:
        messages.error(request, 'O carrinho está vazio.')
        return redirect('carrinho_ver')

    cliente_id = request.POST.get('cliente_id')
    if not cliente_id:
        messages.error(request, 'Selecione o cliente antes de finalizar o pedido.')
        return redirect('carrinho_ver')

    try:
        with transaction.atomic():
            pedido = Pedido.objects.create(
                cliente_id=cliente_id,
                atendente=request.user,
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
                    motivo=f'Venda - Pedido #{pedido.pk}',
                    usuario=request.user,
                )

        carrinho.limpar()
        messages.success(request, f'Pedido #{pedido.pk} finalizado com sucesso!')
        return redirect('pedido_confirmado', pk=pedido.pk)

    except ValidationError as e:
        messages.error(request, str(e))
        return redirect('carrinho_ver')

    
@user_passes_test(eh_funcionario, login_url='login')
def pedido_confirmado(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    return render(request, 'painel/pedidos/pedido_confirmado.html', {'pedido': pedido})

@user_passes_test(eh_funcionario, login_url='login')
def pedido_list(request):
    pedidos = Pedido.objects.select_related('atendente', 'cliente').prefetch_related('itens__variacao').all()

    status = request.GET.get('status')
    if status:
        pedidos = pedidos.filter(status=status)

    return render(request, 'painel/pedidos/pedidos_list.html', {
        'pedidos': pedidos,
        'status_filtro': status,
        'status_choices': Pedido.STATUS_CHOICES,
    })


@user_passes_test(eh_funcionario, login_url='login')
def pedido_confirmado(request, pk):
    pedido = get_object_or_404(
        Pedido.objects.select_related('cliente', 'atendente').prefetch_related('itens__variacao'),
        pk=pk
    )
    return render(request, 'painel/pedidos/pedido_confirmado.html', {'pedido': pedido})