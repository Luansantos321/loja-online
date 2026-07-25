from django.db import models
from .produto import Produto
from django.conf import settings


from django.db import models


class VariacaoProduto(models.Model):
    produto = models.ForeignKey(
        Produto, on_delete=models.CASCADE, related_name='variacoes'
    )
    tamanho = models.CharField(max_length=20, blank=True)
    cor = models.CharField(max_length=40, blank=True)
    sku = models.CharField(max_length=50, unique=True, blank=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade = models.PositiveIntegerField(default=0)
    imagem = models.ImageField(upload_to='variacoes/', blank=True, null=True)

    class Meta:
        unique_together = ('produto', 'tamanho', 'cor')

    @property
    def imagem_exibicao(self):
        if self.imagem:
            return self.imagem.url
        primeira_imagem = self.produto.imagens.first()
        if primeira_imagem:
            return primeira_imagem.imagem.url
        return None

    def __str__(self):
        partes = [self.produto.nome]
        if self.tamanho:
            partes.append(self.tamanho)
        if self.cor:
            partes.append(self.cor)
        return ' - '.join(partes)


class MovimentacaoEstoque(models.Model):
    ENTRADA = 'ENTRADA'
    SAIDA = 'SAIDA'
    TIPO_CHOICES = [
        (ENTRADA, 'Entrada'),
        (SAIDA, 'Saída'),
    ]

    variacao = models.ForeignKey(
        VariacaoProduto, on_delete=models.PROTECT, related_name='movimentacoes'
    )
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    quantidade = models.PositiveIntegerField()
    motivo = models.CharField(
        max_length=100,
        blank=True,
        help_text='Ex: Venda #123, Compra fornecedor X, Ajuste de inventário'
    )
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-criado_em']

    def __str__(self):
        sinal = '+' if self.tipo == self.ENTRADA else '-'
        return f'{self.variacao} {sinal}{self.quantidade}'