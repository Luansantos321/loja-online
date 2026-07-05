from django.db import models
from .produto import Produto


class ImagemProduto(models.Model):
    produto = models.ForeignKey(
        Produto,
        on_delete=models.CASCADE,
        related_name="imagens"
    )

    imagem = models.ImageField(
        upload_to="produtos/"
    )

    principal = models.BooleanField(
        default=False
    )

    ordem = models.PositiveIntegerField(
        default=1
    )

    class Meta:
        ordering = ["ordem"]
        verbose_name = "Imagem do Produto"
        verbose_name_plural = "Imagens do Produto"

    def __str__(self):
        return self.produto.nome