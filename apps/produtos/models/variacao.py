from django.db import models
from .produto import Produto


from django.db import models


class VariacaoProduto(models.Model):
    produto = models.ForeignKey(
        "produtos.Produto",
        on_delete=models.CASCADE,
        related_name="variacoes"
    )
    sku = models.CharField(max_length=50, unique=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    estoque = models.PositiveIntegerField(default=0)
    ativo = models.BooleanField(default=True)


    class Meta:
        verbose_name = "Variação do Produto"
        verbose_name_plural = "Variações do Produto"

    def __str__(self):
        return f"{self.produto.nome} - {self.sku}"