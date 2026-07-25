from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Categoria


def categoria_list(request):
    categorias = Categoria.objects.all().order_by('nome')
    return render(request, 'painel/categorias/categoria_list.html', {
        'categorias': categorias
    })


def categoria_create(request):
    if request.method == 'POST':
        nome = request.POST.get('nome', '').strip()

        if not nome:
            messages.error(request, 'O nome da categoria é obrigatório.')
            return render(request, 'painel/categorias/categoria_form.html', {
                'titulo': 'Nova Categoria',
                'nome': nome
            })

        if Categoria.objects.filter(nome__iexact=nome).exists():
            messages.error(request, 'Já existe uma categoria com esse nome.')
            return render(request, 'painel/categorias/categoria_form.html', {
                'titulo': 'Nova Categoria',
                'nome': nome
            })

        Categoria.objects.create(nome=nome)
        messages.success(request, 'Categoria cadastrada com sucesso!')
        return redirect('categoria_list')

    return render(request, 'painel/categorias/categoria_form.html', {
        'titulo': 'Nova Categoria'
    })


def categoria_update(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)

    if request.method == 'POST':
        nome = request.POST.get('nome', '').strip()

        if not nome:
            messages.error(request, 'O nome da categoria é obrigatório.')
            return render(request, 'painel/categorias/categoria_form.html', {
                'titulo': 'Editar Categoria',
                'nome': nome,
                'categoria': categoria
            })

        if Categoria.objects.filter(nome__iexact=nome).exclude(pk=categoria.pk).exists():
            messages.error(request, 'Já existe uma categoria com esse nome.')
            return render(request, 'painel/categorias/categoria_form.html', {
                'titulo': 'Editar Categoria',
                'nome': nome,
                'categoria': categoria
            })

        categoria.nome = nome
        # força o slug a ser recalculado com base no novo nome
        categoria.slug = ''
        categoria.save()

        messages.success(request, 'Categoria atualizada com sucesso!')
        return redirect('categoria_list')

    return render(request, 'painel/categorias/categoria_form.html', {
        'titulo': 'Editar Categoria',
        'categoria': categoria
    })


def categoria_delete(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)

    if request.method == 'POST':
        categoria.delete()
        messages.success(request, 'Categoria excluída com sucesso!')
        return redirect('categoria_list')

    return render(request, 'painel/categorias/categoria_confirm_delete.html', {
        'categoria': categoria
    })