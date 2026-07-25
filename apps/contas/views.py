from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from .models import Usuario
from django.contrib import messages
from django.contrib.auth import login



def eh_funcionario(user):
    return user.is_authenticated and user.is_staff

def cadastro_cliente(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        telefone = request.POST.get('telefone', '').strip()
        senha = request.POST.get('senha', '')
        senha_confirmacao = request.POST.get('senha_confirmacao', '')

        erros = []
        if not username or not email or not senha:
            erros.append('Preencha usuário, e-mail e senha.')
        if senha != senha_confirmacao:
            erros.append('As senhas não coincidem.')
        if len(senha) < 8:
            erros.append('A senha precisa ter pelo menos 8 caracteres.')
        if Usuario.objects.filter(username=username).exists():
            erros.append('Esse nome de usuário já está em uso.')
        if Usuario.objects.filter(email=email).exists():
            erros.append('Esse e-mail já está cadastrado.')

        if erros:
            for erro in erros:
                messages.error(request, erro)
            return render(request, 'contas/cadastro.html', {
                'username': username, 'email': email,
                'first_name': first_name, 'telefone': telefone,
            })

        cliente = Usuario(
            username=username,
            email=email,
            first_name=first_name,
            telefone=telefone,
            is_staff=False,
        )
        cliente.set_password(senha)
        cliente.save()

        login(request, cliente)
        messages.success(request, f'Bem-vindo(a), {cliente.first_name or cliente.username}!')
        return redirect('lista_produtos')

    return render(request, 'painel/contas/cadastro.html')

@user_passes_test(eh_funcionario, login_url='login')
def cliente_list(request):
    clientes = Usuario.objects.filter(is_staff=False)

    busca = request.GET.get('busca')
    if busca:
        clientes = clientes.filter(
            first_name__icontains=busca
        ) | clientes.filter(
            last_name__icontains=busca
        ) | clientes.filter(
            email__icontains=busca
        )

    return render(request, 'painel/contas/cliente_list.html', {
        'clientes': clientes,
        'busca': busca or '',
    })


@user_passes_test(eh_funcionario, login_url='login')
def cliente_detalhe(request, pk):
    cliente = get_object_or_404(Usuario, pk=pk, is_staff=False)
    compras = cliente.compras.prefetch_related('itens__variacao').all()
    return render(request, 'painel/contas/cliente_detalhe.html', {
        'cliente': cliente,
        'compras': compras,
    })