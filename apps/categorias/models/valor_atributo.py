from django.db import models

from .atributo import Atributo


class ValorAtributo(models.Model):
    atributo = models.ForeignKey(
        Atributo,
        on_delete=models.CASCADE,
        related_name="valores"
    )

    valor = models.CharField(
        max_length=100
    )

    slug = models.SlugField(
        unique=True
    )

    class Meta:
        verbose_name = "Valor do Atributo"
        verbose_name_plural = "Valores dos Atributos"
        unique_together = ("atributo", "valor")
        ordering = ["atributo", "valor"]

    def __str__(self):
        return f"{self.atributo.nome}: {self.valor}"