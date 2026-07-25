from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.text import slugify

from django.contrib.auth.decorators import login_required, user_passes_test

from apps.produtos.models import Marca, ImagemProduto , MovimentacaoEstoque, VariacaoProduto
from apps.produtos.models import Produto
from apps.categorias.models import Categoria
from django.db import transaction

def administrador(user):
    return user.is_authenticated and user.is_staff

@login_required
def dashboard(request):

    return render(request, "painel/dashboard.html")


@login_required
@user_passes_test(administrador)
def marcas_lista(request):

    busca = request.GET.get("q")

    marcas = Marca.objects.all().order_by("nome")

    if busca:
        marcas = marcas.filter(nome__icontains=busca)

    return render(
        request,
        "painel/marcas/lista.html",
        {
            "marcas": marcas,
            "busca": busca
        }
    )

@login_required
@user_passes_test(administrador)
def marca_nova(request):

    if request.method == "POST":

        nome = request.POST.get("nome")
        descricao = request.POST.get("descricao")
        ativa = True if request.POST.get("ativa") else False

        logo = None

        if "logo" in request.FILES:
            logo = request.FILES["logo"]

        Marca.objects.create(
            nome=nome,
            descricao=descricao,
            ativa=ativa,
            logo=logo
        )

        messages.success(
            request,
            "Marca cadastrada com sucesso."
        )

        return redirect("painel_marcas")

    return render(
        request,
        "painel/marcas/formulario.html"
    )



@login_required
@user_passes_test(administrador)
def marca_editar(request, pk):

    marcas = get_object_or_404(
        Marca,
        pk=pk
    )

    if request.method == "POST":

        marcas.nome = request.POST.get("nome")
        marcas.descricao = request.POST.get("descricao")
        marcas.ativa = True if request.POST.get("ativa") else False

        if "logo" in request.FILES:
            marcas.logo = request.FILES["logo"]

        marcas.save()

        messages.success(
            request,
            "Marca atualizada."
        )

        return redirect("painel_marcas")

    return render(
        request,
        "painel/marcas/formulario.html",
        {
            "marcas": marcas
        }
    )



@login_required
@user_passes_test(administrador)
def marca_excluir(request, pk):

    marcas = get_object_or_404(
        Marca,
        pk=pk
    )

    if request.method == "POST":

        marcas.delete()

        messages.success(
            request,
            "Marca excluída."
        )

        return redirect("painel_marcas")

    return render(
        request,
        "painel/marcas/excluir.html",
        {
            "marcas": marcas
        }
    )

@login_required
def produtos_lista(request):

    produtos = Produto.objects.all().order_by("-id")

    context = {

        "produtos": produtos

    }

    return render(

        request,

        "painel/produtos/lista.html",

        context

    )


@login_required
def produto_novo(request):

    categorias = Categoria.objects.all()
    marcas = Marca.objects.all()

    if request.method == "POST":

        nome = request.POST.get("nome")
        imagem  = None

        if "imagem" in request.FILES:
            imagem = request.FILES["imagem"]
        descricao = request.POST.get("descricao")
        categoria = request.POST.get("categoria")
        marcas = Marca.objects.get(pk=request.POST.get("marca"))

        ativo = True if request.POST.get("ativo") else False
        destaque = True if request.POST.get("destaque") else False
        lancamento = True if request.POST.get("lancamento") else False
        mais_vendido = True if request.POST.get("mais_vendido") else False

        slug = slugify(nome)

        produto = Produto.objects.create(

            categoria_id=categoria,

            nome=nome,

            marca=marcas,

            slug=slug,

            descricao=descricao,

            ativo=ativo,

            destaque=destaque,

            lancamento=lancamento,

            mais_vendido=mais_vendido,

        )
        if imagem:
            ImagemProduto.objects.create(
                produto=produto,
                imagem=imagem,
                principal=True,
                ordem=1
            )

        messages.success(

            request,

            "Produto cadastrado com sucesso."

        )

        return redirect("detalhe_produto", produto.pk)

    return render(

        request,

        "painel/produtos/formulario.html",

        {

            "categorias": categorias,
            "marcas": marcas

        }

    )
@login_required
def produto_detalhe(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    return render(
        request,
        "painel/produtos/detalhes.html",
        {"produto": produto}
    )

@login_required
def produto_excluir_definitivo(request, pk):
    produto = get_object_or_404(Produto, pk=pk)

    if request.method == 'POST':
        with transaction.atomic():
            variacoes = VariacaoProduto.objects.filter(produto=produto)
            MovimentacaoEstoque.objects.filter(variacao__in=variacoes).delete()
            variacoes.delete()

            nome_produto = produto.nome
            produto.delete()

        messages.success(request, f'Produto "{nome_produto}" excluído definitivamente, junto com variações e histórico.')
        return redirect('painel_produtos')

    return render(request, 'painel/produtos/confirmar_exclusao_definitiva.html', {'produto': produto})


@login_required
def produto_editar(request, pk):

    produto = get_object_or_404(

        Produto,

        pk=pk

    )

    categorias = Categoria.objects.all()

    marcas = Marca.objects.all()

    if request.method == "POST":

        produto.nome = request.POST.get("nome")

        produto.descricao = request.POST.get("descricao")

        produto.categoria_id = request.POST.get("categoria")

        produto.marcas = request.POST.get("marcas")

        produto.slug = slugify(produto.nome)

        produto.ativo = True if request.POST.get("ativo") else False

        produto.destaque = True if request.POST.get("destaque") else False

        produto.lancamento = True if request.POST.get("lancamento") else False

        produto.mais_vendido = True if request.POST.get("mais_vendido") else False

        produto.save()

        messages.success(

            request,

            "Produto atualizado."

        )

        return redirect(

            "painel_produtos" ,produto.pk)

    return render(

        request,

        "painel/produtos/formulario.html",

        {

            "produto": produto,

            "categorias": categorias,

            "marcas": marcas,

        }

    )


@login_required
def produto_excluir(request, pk):

    produto = get_object_or_404(

        Produto,

        pk=pk

    )

    if request.method == "POST":

        produto.delete()

        messages.success(

            request,

            "Produto excluído."

        )

        return redirect(

            "painel_produto_excluir", produto.pk)

    return render(

        request,

        "painel/produtos/excluir.html",

        {

            "produto": produto

        }

    )