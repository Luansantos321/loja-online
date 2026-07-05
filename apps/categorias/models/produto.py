from django.db import models


class Produto(models.Model):
    categoria = models.ForeignKey(
        "categorias.Categoria",
        on_delete=models.PROTECT,
        related_name="produtos"
    )

    nome = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    descricao = models.TextField()
    ativo = models.BooleanField(default=True)

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        ordering = ["nome"]

    def __str__(self):
        return self.nome