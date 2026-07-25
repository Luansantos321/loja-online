from decimal import Decimal
from apps.produtos.models import VariacaoProduto

SESSION_KEY = 'carrinho'


class Carrinho:
    def __init__(self, request):
        self.session = request.session
        carrinho = self.session.get(SESSION_KEY)
        if not carrinho:
            carrinho = self.session[SESSION_KEY] = {}
        self.carrinho = carrinho

    def adicionar(self, variacao_id, quantidade=1):
        variacao_id = str(variacao_id)
        if variacao_id in self.carrinho:
            self.carrinho[variacao_id]['quantidade'] += quantidade
        else:
            variacao = VariacaoProduto.objects.get(pk=variacao_id)
            self.carrinho[variacao_id] = {
                'quantidade': quantidade,
                'preco': str(variacao.preco),
            }
        self.salvar()

    def remover(self, variacao_id):
        variacao_id = str(variacao_id)
        if variacao_id in self.carrinho:
            del self.carrinho[variacao_id]
            self.salvar()

    def limpar(self):
        self.session[SESSION_KEY] = {}
        self.salvar()

    def salvar(self):
        self.session.modified = True

    def __iter__(self):
        variacao_ids = self.carrinho.keys()
        variacoes = VariacaoProduto.objects.filter(pk__in=variacao_ids)
        mapa = {str(v.pk): v for v in variacoes}

        for variacao_id, dados in self.carrinho.items():
            variacao = mapa.get(variacao_id)
            if not variacao:
                continue
            preco = Decimal(dados['preco'])
            quantidade = dados['quantidade']
            yield {
                'variacao': variacao,
                'quantidade': quantidade,
                'preco': preco,
                'subtotal': preco * quantidade,
            }

    def total(self):
        return sum(item['subtotal'] for item in self)

    def __len__(self):
        return sum(item['quantidade'] for item in self.carrinho.values())