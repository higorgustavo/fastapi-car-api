# Estrutura do Projeto

Esta seção descreve a organização de diretórios e arquivos do projeto.

## Árvore de Diretórios

```
car_api/
├── .gitignore              # Arquivos ignorados pelo Git
├── alembic.ini             # Configuração do Alembic (migrações)
├── mkdocs.yml              # Configuração da documentação MkDocs
├── poetry.lock             # Lockfile de dependências
├── pyproject.toml          # Configuração do projeto e dependências
├── README.md               # README do repositório
├── docs/                   # Documentação do projeto (MkDocs)
│   ├── index.md            # Página inicial da documentação
│   ├── overview.md         # Visão geral
│   ├── prerequisites.md    # Pré-requisitos
│   ├── installation.md     # Instalação
│   ├── configuration.md    # Configuração
│   ├── guidelines.md       # Guidelines e padrões
│   ├── structure.md        # Estrutura do projeto
│   ├── api-endpoints.md    # API Endpoints
│   ├── system-modeling.md  # Modelagem do sistema
│   ├── authentication.md   # Autenticação e segurança
│   ├── development.md      # Desenvolvimento
│   ├── testing.md          # Testes
│   ├── deployment.md       # Deploy
│   ├── contributing.md     # Contribuição
│   └── release-notes.md    # Release notes
├── migrations/             # Migrações do Alembic
│   ├── env.py              # Configuração do ambiente de migração
│   ├── README              # README do Alembic
│   ├── script.py.mako      # Template para novas migrações
│   └── versions/           # Arquivos de migração
├── tests/                  # Testes automatizados
│   └── __init__.py
└── car_api/                # Código fonte da aplicação
    ├── __init__.py
    ├── app.py              # Ponto de entrada do FastAPI
    ├── core/               # Configurações centrais
    │   ├── database.py     # Conexão com banco de dados
    │   ├── security.py     # Autenticação e segurança
    │   └── settings.py     # Configurações via variáveis de ambiente
    ├── models/             # Modelos do banco de dados (SQLAlchemy)
    │   ├── __init__.py     # Exportação dos modelos
    │   ├── base.py         # Classe base DeclarativeBase
    │   ├── cars.py         # Modelos Car e Brand
    │   └── users.py        # Modelo User
    ├── routers/            # Handlers de rota (endpoints)
    │   ├── auth.py         # Endpoints de autenticação
    │   ├── brands.py       # Endpoints de marcas
    │   ├── cars.py         # Endpoints de carros
    │   └── users.py        # Endpoints de usuários
    └── schemas/            # Schemas de validação (Pydantic)
        ├── auth.py         # Schemas de autenticação
        ├── brands.py       # Schemas de marcas
        ├── cars.py         # Schemas de carros
        └── users.py        # Schemas de usuários
```

## Descrição dos Diretórios

### `/car_api` - Código Fonte da Aplicação

Contém todo o código fonte da API, organizado em submódulos.

#### `/car_api/core` - Núcleo Central

| Arquivo | Descrição |
|---------|-----------|
| `database.py` | Configuração do engine assíncrono e sessão do SQLAlchemy |
| `security.py` | Funções de hash, verificação, JWT e autorização |
| `settings.py` | Classe Settings com variáveis de ambiente via Pydantic |

#### `/car_api/models` - Modelos de Dados

Modelos SQLAlchemy que representam as tabelas do banco de dados.

| Arquivo | Modelos |
|---------|---------|
| `base.py` | Classe `Base` (DeclarativeBase) |
| `users.py` | `User` - Usuários do sistema |
| `cars.py` | `Car`, `Brand`, `FuelType`, `TransmissionType` |

#### `/car_api/routers` - Endpoints da API

Handlers HTTP organizados por domínio.

| Arquivo | Endpoints |
|---------|-----------|
| `auth.py` | `/token`, `/refresh_token` |
| `users.py` | CRUD completo de usuários |
| `brands.py` | CRUD completo de marcas |
| `cars.py` | CRUD de carros + transferência |

#### `/car_api/schemas` - Schemas Pydantic

Modelos de validação de entrada e saída da API.

| Arquivo | Schemas |
|---------|---------|
| `auth.py` | `Token`, `LoginRequest` |
| `users.py` | `UserSchema`, `UserPublicSchema`, `UserUpdateSchema`, `UserListPublicSchema` |
| `cars.py` | `CarSchema`, `CarPublicSchema`, `CarUpdateSchema`, `CarListPublicSchema`, `CarTransferSchema` |
| `brands.py` | `BrandSchema`, `BrandPublicSchema`, `BrandUpdateSchema`, `BrandListPublicSchema` |

### `/migrations` - Migrações do Banco de Dados

Gerenciado pelo Alembic para versionamento do schema.

| Arquivo | Descrição |
|---------|-----------|
| `env.py` | Configuração do ambiente assíncrono |
| `script.py.mako` | Template para geração de migrações |
| `versions/` | Arquivos de migração gerados automaticamente |

### `/tests` - Testes

Contém os testes automatizados da aplicação.

### `/docs` - Documentação

Documentação do projeto em Markdown, servida via MkDocs + Material.

## Arquivos de Configuração na Raiz

| Arquivo | Propósito |
|---------|-----------|
| `.gitignore` | Lista arquivos ignorados pelo Git (.env, .venv, __pycache__, etc.) |
| `alembic.ini` | Configuração base do Alembic |
| `mkdocs.yml` | Configuração do MkDocs (tema, navegação, plugins) |
| `poetry.lock` | Versões exatas das dependências (commitado) |
| `pyproject.toml` | Dependências, scripts, configuração do Ruff |
| `README.md` | Introdução ao projeto |
