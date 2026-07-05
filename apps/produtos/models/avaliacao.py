from django.db import models
from django.conf import settings
from ..models import Produto


class Avaliacao(models.Model):
    produto = models.ForeignKey(
        Produto,
        on_delete=models.CASCADE,
        related_name="avaliacoes"
    )

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="avaliacoes"
    )

    nota = models.PositiveSmallIntegerField()

    comentario = models.TextField(
        blank=True
    )

    criado_em = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = "Avaliação"
        verbose_name_plural = "Avaliações"
        unique_together = ("produto", "usuario")

    def __str__(self):
        return f"{self.produto.nome} - {self.nota}"