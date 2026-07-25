from django.db import transaction
from django.core.exceptions import ValidationError
from .models import VariacaoProduto, MovimentacaoEstoque



@transaction.atomic
def registrar_entrada(variacao_id, quantidade, motivo='', usuario=None):
    if quantidade <= 0:
        raise ValidationError('A quantidade deve ser maior que zero.')

    # select_for_update trava a linha até o fim da transação,
    # evitando que duas requisições simultâneas leiam o mesmo saldo
    # antigo e gerem um valor final errado.
    variacao = VariacaoProduto.objects.select_for_update().get(pk=variacao_id)

    variacao.quantidade += quantidade
    variacao.save(update_fields=['quantidade'])

    MovimentacaoEstoque.objects.create(
        variacao=variacao,
        tipo=MovimentacaoEstoque.ENTRADA,
        quantidade=quantidade,
        motivo=motivo,
        usuario=usuario,
    )
    return variacao


@transaction.atomic
def registrar_saida(variacao_id, quantidade, motivo='', usuario=None):
    if quantidade <= 0:
        raise ValidationError('A quantidade deve ser maior que zero.')

    variacao = VariacaoProduto.objects.select_for_update().get(pk=variacao_id)

    if variacao.quantidade < quantidade:
        raise ValidationError(
            f'Estoque insuficiente. Disponível: {variacao.quantidade}, solicitado: {quantidade}.'
        )

    variacao.quantidade -= quantidade
    variacao.save(update_fields=['quantidade'])

    MovimentacaoEstoque.objects.create(
        variacao=variacao,
        tipo=MovimentacaoEstoque.SAIDA,
        quantidade=quantidade,
        motivo=motivo,
        usuario=usuario,
    )
    return variacao