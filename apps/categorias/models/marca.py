from django.db import models


class Marca(models.Model):
    nome = models.CharField(
        max_length=100,
        unique=True
    )

    slug = models.SlugField(
        unique=True
    )

    ativa = models.BooleanField(
        default=True
    )

    criada_em = models.DateTimeField(
        auto_now_add=True
    )

    atualizada_em = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["nome"]
        verbose_name = "Marca"
        verbose_name_plural = "Marcas"

    def __str__(self):
        return self.nome