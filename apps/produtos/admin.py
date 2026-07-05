# IMPORTS
from django.contrib import admin
from .models import (
    Produto, Marca, ImagemProduto,
    VariacaoProduto, Atributo,
    ValorAtributo, VariacaoAtributo,
    Avaliacao
)

# INLINE IMAGENS
class ImagemProdutoInline(admin.TabularInline):
    model = ImagemProduto
    extra = 1


# INLINE VARIAÇÕES
class VariacaoProdutoInline(admin.TabularInline):
    model = VariacaoProduto
    extra = 1


# PRODUTO
@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ("nome", "categoria", "ativo")
    inlines = [ImagemProdutoInline, VariacaoProdutoInline]


# MARCA
@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ("nome",)


# ATRIBUTOS
@admin.register(Atributo)
class AtributoAdmin(admin.ModelAdmin):
    list_display = ("nome",)


# VALORES
@admin.register(ValorAtributo)
class ValorAtributoAdmin(admin.ModelAdmin):
    list_display = ("atributo", "valor")


# VARIAÇÕES
@admin.register(VariacaoProduto)
class VariacaoProdutoAdmin(admin.ModelAdmin):
    list_display = ("produto", "sku", "preco", "estoque")


# AVALIAÇÕES
@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ("produto", "usuario", "nota")