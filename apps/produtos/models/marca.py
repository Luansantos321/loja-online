from django.db import models
from django.utils.text import slugify


class Marca(models.Model):

    nome = models.CharField(
        max_length=120,
        unique=True,
        verbose_name="Nome"
    )

    slug = models.SlugField(
        unique=True,
        blank=True
    )

    descricao = models.TextField(
        blank=True
    )

    logo = models.ImageField(
        upload_to="marcas/",
        blank=True,
        null=True
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

    def save(self, *args, **kwargs):

        if not self.slug:

            self.slug = slugify(self.nome)

        super().save(*args, **kwargs)

    def __str__(self):

        return self.nome