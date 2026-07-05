from django.db import models
from .produto import Produto


class VariacaoProduto(models.Model):
    produto = models.ForeignKey(
        Produto,
        on_delete=models.CASCADE,
        related_name="variacoes"
    )

    sku = models.CharField(
        max_length=100,
        unique=True
    )

    preco = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    estoque = models.PositiveIntegerField(
        default=0
    )

    ativo = models.BooleanField(
        default=True
    )

    criado_em = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = "Variação do Produto"
        verbose_name_plural = "Variações do Produto"

    def __str__(self):
        return f"{self.produto.nome} - {self.sku}"