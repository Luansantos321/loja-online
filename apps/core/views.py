from django.shortcuts import render
from apps.produtos.models import Produto


def home(request):
    produtos_base = Produto.objects.filter(ativo=True).select_related('categoria').prefetch_related('imagens', 'variacoes')

    destaques = produtos_base.filter(destaque=True)[:8]
    lancamentos = produtos_base.filter(lancamento=True).order_by('-criado_em')[:8]
    mais_vendidos = produtos_base.filter(mais_vendido=True)[:8]

    context = {
        "destaques": destaques,
        "lancamentos": lancamentos,
        "mais_vendidos": mais_vendidos,
    }

    return render(request, "core/home.html", context)