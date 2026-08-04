# Loja Online

Sistema web de e-commerce desenvolvido com Python e Django, projetado para gerenciar produtos, categorias, estoque e pedidos em uma única plataforma.

O projeto está sendo desenvolvido com foco em boas práticas de desenvolvimento, organização do código e escalabilidade, simulando funcionalidades encontradas em sistemas utilizados por empresas do setor de comércio eletrônico.

## Status do Projeto

🚧 Em desenvolvimento

Novas funcionalidades estão sendo implementadas continuamente com o objetivo de evoluir o sistema e aplicar conceitos de desenvolvimento back-end utilizando Django.

## Funcionalidades

### Catálogo de Produtos

- Cadastro de produtos
- Edição de produtos
- Exclusão lógica
- Controle de produtos ativos e inativos
- Cadastro de categorias
- Cadastro de marcas
- Controle de imagens dos produtos

### Controle de Estoque

- Cadastro de variações
- Entrada de estoque
- Saída de estoque
- Controle de quantidade disponível
- Histórico de movimentações

### Painel Administrativo

- Dashboard administrativo
- Gerenciamento de produtos
- Gerenciamento de categorias
- Gerenciamento de estoque
- Controle de usuários

### Loja Virtual

- Listagem de produtos
- Página de detalhes
- Pesquisa de produtos
- Organização por categorias

## Tecnologias

### Back-end

- Python
- Django

### Banco de Dados

- PostgreSQL
- SQLite (desenvolvimento)

### Front-end

- HTML5
- CSS3
- Bootstrap
- JavaScript

### Ferramentas

- Git
- GitHub

## Estrutura do Projeto

```text
loja-online/

├── core/
├── produtos/
├── categorias/
├── pedidos/
├── usuarios/
├── templates/
├── static/
├── media/
├── manage.py
└── requirements.txt
```

## Executando o Projeto

Clone o repositório

```bash
git clone https://github.com/Luansantos321/loja-online.git
```

Entre na pasta

```bash
cd loja-online
```

Crie um ambiente virtual

```bash
python -m venv venv
```

Ative o ambiente

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

Instale as dependências

```bash
pip install -r requirements.txt
```

Execute as migrações

```bash
python manage.py migrate
```

Inicie o servidor

```bash
python manage.py runserver
```

## Arquitetura

A aplicação foi desenvolvida utilizando a arquitetura MTV do Django, mantendo a separação entre modelos, regras de negócio e interface.

O projeto possui estrutura modular, facilitando a manutenção do código e permitindo a implementação de novas funcionalidades sem comprometer a organização da aplicação.

## Conhecimentos Aplicados

Durante o desenvolvimento deste projeto estão sendo aplicados conhecimentos relacionados a:

- Programação Orientada a Objetos
- Desenvolvimento Web com Django
- Modelagem de Banco de Dados
- Relacionamentos entre modelos
- CRUD completo
- Controle de estoque
- Organização modular de aplicações Django
- Versionamento com Git e GitHub
- Boas práticas de desenvolvimento
- Estruturação de aplicações escaláveis

## Roadmap

Funcionalidades planejadas para as próximas versões:

- Sistema de autenticação de clientes
- Carrinho de compras
- Lista de desejos
- Checkout
- Integração com meios de pagamento
- Controle de pedidos
- Área do cliente
- Relatórios administrativos
- API REST
- Dashboard com indicadores

## Objetivo do Projeto

O objetivo deste projeto é desenvolver uma plataforma de comércio eletrônico capaz de gerenciar produtos, estoque e pedidos, aplicando conceitos de desenvolvimento web e arquitetura de software utilizados em aplicações reais.

Além de servir como ambiente de aprendizado, o projeto busca simular cenários encontrados em sistemas corporativos, priorizando organização, escalabilidade e boas práticas de desenvolvimento.

## Autor

**Luan Santos da Silva**

Graduado em Gestão da Tecnologia da Informação.

Atualmente desenvolvendo aplicações web com Python e Django e estudando Java e Spring Boot.

- GitHub: https://github.com/Luansantos321
- Portfólio: https://luansantos-portfolio.vercel.app/
- LinkedIn: www.linkedin.com/in/luan-santos-da-silva-1414ab369
- E-mail: luansantosdasilva77@gmail.com

## Licença

Este projeto está licenciado sob a licença MIT. Consulte o arquivo `LICENSE` para mais informações.
