from django.db import models


class Atributo(models.Model):
    nome = models.CharField(
        max_length=100,
        unique=True
    )

    slug = models.SlugField(
        unique=True
    )

    criado_em = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = "Atributo"
        verbose_name_plural = "Atributos"
        ordering = ["nome"]

    def __str__(self):
        return self.nome