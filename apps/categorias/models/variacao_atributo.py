from django.db import models

from .variacao import VariacaoProduto
from .valor_atributo import ValorAtributo


class VariacaoAtributo(models.Model):
    variacao = models.ForeignKey(
        VariacaoProduto,
        on_delete=models.CASCADE,
        related_name="atributos"
    )

    valor = models.ForeignKey(
        ValorAtributo,
        on_delete=models.PROTECT
    )

    class Meta:
        verbose_name = "Atributo da Variação"
        verbose_name_plural = "Atributos das Variações"
        unique_together = ("variacao", "valor")

    def __str__(self):
        return f"{self.variacao} - {self.valor}"