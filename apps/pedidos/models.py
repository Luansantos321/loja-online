from django.db import models
from django.conf import settings
from apps.produtos.models import VariacaoProduto


class Pedido(models.Model):
    ABERTO = 'ABERTO'
    FINALIZADO = 'FINALIZADO'
    CANCELADO = 'CANCELADO'
    STATUS_CHOICES = [
        (ABERTO, 'Aberto'),
        (FINALIZADO, 'Finalizado'),
        (CANCELADO, 'Cancelado'),
    ]
    cliente = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True,
        related_name='compras'
    )

    atendente = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='pedidos'
    )
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default=ABERTO)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-criado_em']

    def __str__(self):
        return f'Pedido #{self.pk} - {self.get_status_display()}'

    @property
    def total(self):
        return sum(item.subtotal for item in self.itens.all())


class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens')
    variacao = models.ForeignKey(VariacaoProduto, on_delete=models.PROTECT)
    quantidade = models.PositiveIntegerField()
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.quantidade}x {self.variacao}'

    @property
    def subtotal(self):
        return self.quantidade * self.preco_unitario