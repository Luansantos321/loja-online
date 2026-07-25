from django.db import models
from django.utils import timezone
from .marca import Marca


class Produto(models.Model):
    categoria = models.ForeignKey(
        "categorias.Categoria",
        on_delete=models.PROTECT,
        related_name="produtos"
    )
    marca = models.ForeignKey(Marca,
    on_delete=models.PROTECT,
    related_name="produtos",
    null=True,
    blank=True,
)
    nome = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    descricao = models.TextField()
    ativo = models.BooleanField(default=True)
    destaque = models.BooleanField(default=False)
    lancamento = models.BooleanField(default=False)
    mais_vendido = models.BooleanField(default=False)
    data_criacao = models.DateTimeField(default=timezone.now)
    criado_em = models.DateTimeField(default=timezone.now)
    atualizado_em = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        ordering = ["nome"]

    @property
    def preco_minimo(self):
        variacao = self.variacoes.order_by('preco').first()
        return variacao.preco if variacao else None

    def __str__(self):
        return self.nome