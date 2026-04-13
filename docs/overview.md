# Visão Geral

## Sobre o Projeto

O **Car API** é uma API REST moderna e completa desenvolvida com FastAPI para gerenciamento de veículos automotores. O sistema permite o cadastro e gerenciamento de carros, marcas e usuários, com autenticação via JWT e controle de acesso baseado em propriedade.

## Propósito

O projeto foi criado para fornecer uma solução robusta de gerenciamento de carros com as seguintes características:

- **CRUD Completo**: Operações de criação, leitura, atualização e remoção para carros, marcas e usuários
- **Autenticação Segura**: Sistema de autenticação baseado em tokens JWT
- **Autorização por Propriedade**: Controle de acesso onde usuários só podem modificar seus próprios carros
- **Transferência de Propriedade**: Funcionalidade para transferir carros entre usuários
- **Validação Rigorosa**: Validações de dados via Pydantic com regras de negócio específicas
- **Banco de Dados Assíncrono**: Operações de I/O não-bloqueantes com SQLAlchemy Async

## Funcionalidades Principais

### Usuários
- Registro de novos usuários
- Autenticação via e-mail e senha
- Listagem com paginação e busca
- Atualização de dados cadastrais
- Remoção de contas

### Autenticação
- Geração de tokens JWT
- Refresh de tokens expirados
- Proteção de rotas via Bearer Token

### Marcas
- Cadastro de marcas de veículos
- Listagem com filtros e busca
- Atualização e remoção (com validação de dependência)

### Carros
- Cadastro completo de veículos (modelo, ano, cor, placa, etc.)
- Listagem com múltiplos filtros (marca, proprietário, combustível, preço)
- Atualização parcial ou total
- Transferência entre proprietários
- Exclusão com validação de propriedade

## Arquitetura

O projeto segue uma arquitetura limpa e bem organizada:

- **Routers**: Handlers de requisição HTTP organizados por domínio (auth, users, brands, cars)
- **Schemas**: Modelos de validação de entrada/saída com Pydantic
- **Models**: Modelos de banco de dados com SQLAlchemy ORM
- **Core**: Configurações centrais, conexão com banco e segurança

## Stack Tecnológica

| Camada | Tecnologia |
|--------|-----------|
| Framework Web | FastAPI |
| Validação | Pydantic |
| ORM | SQLAlchemy (Async) |
| Banco de Dados | SQLite (aiosqlite) |
| Migrações | Alembic |
| Autenticação | JWT (PyJWT) |
| Hash de Senha | pwdlib (Argon2) |
| Linting | Ruff |
| Task Runner | Taskipy |
| Documentação | MkDocs + Material |
