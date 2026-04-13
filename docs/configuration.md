# Configuração do Projeto

## Variáveis de Ambiente

Todas as configurações são gerenciadas pela classe `Settings` em `car_api/core/settings.py`, que utiliza Pydantic Settings para carregar variáveis de ambiente.

### Arquivo `.env`

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
# Banco de Dados
DATABASE_URL=sqlite+aiosqlite:///./car_api.db

# JWT (JSON Web Token)
JWT_SECRET_KEY=sua_chave_secreta_aqui
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=30
```

## Configurações Disponíveis

### DATABASE_URL

URL de conexão com o banco de dados no formato SQLAlchemy.

**Formato para SQLite:**
```env
DATABASE_URL=sqlite+aiosqlite:///./car_api.db
```

**Formato para PostgreSQL (produção):**
```env
DATABASE_URL=postgresql+asyncpg://usuario:senha@localhost:5432/nome_db
```

**Formato para MySQL (produção):**
```env
DATABASE_URL=mysql+aiomysql://usuario:senha@localhost:3306/nome_db
```

### JWT_SECRET_KEY

Chave secreta utilizada para assinar os tokens JWT.

> **Importante**: Utilize uma chave forte e única em produção. Gere uma com:
>
> ```bash
> python -c "import secrets; print(secrets.token_urlsafe(32))"
> ```

### JWT_ALGORITHM

Algoritmo de assinatura do token. O padrão é `HS256`.

Algoritmos suportidos:
- `HS256` - HMAC-SHA256 (padrão)
- `HS384` - HMAC-SHA384
- `HS512` - HMAC-SHA512

### JWT_EXPIRATION_MINUTES

Tempo de expiração do token em minutos. O padrão é `30` minutos.

## Banco de Dados

### Migrações com Alembic

O projeto utiliza Alembic para versionamento do schema do banco de dados.

**Criar uma nova migração:**
```bash
poetry run alembic revision --autogenerate -m "descrição da mudança"
```

**Aplicar todas as migrações:**
```bash
poetry run alembic upgrade head
```

**Reverter última migração:**
```bash
poetry run alembic downgrade -1
```

**Ver status das migrações:**
```bash
poetry run alembic current
```

**Histórico de migrações:**
```bash
poetry run alembic history
```

### Configuração do Alembic

O arquivo `alembic.ini` contém a configuração básica, mas a URL do banco é sobrescrita dinamicamente via `Settings` em `migrations/env.py`.

## Servidor de Desenvolvimento

Inicie o servidor com auto-reload:

```bash
poetry run task run
```

Isso executa: `fastapi dev car_api/app.py`

### Opções do FastAPI Dev

- **Host padrão**: `127.0.0.1`
- **Porta padrão**: `8000`
- **Auto-reload**: Ativado por padrão no modo dev

## Documentação MkDocs

Sirva a documentação localmente:

```bash
poetry run task docs
```

A documentação estará disponível em `http://127.0.0.1:8001`.

## Linting e Formatação

**Verificar erros de lint:**
```bash
poetry run task lint
```

**Formatar código automaticamente:**
```bash
poetry run task format
```

O Ruff é configurado em `pyproject.toml` com:
- Comprimento máximo de linha: 79 caracteres
- Aspas simples para strings
- Regras ativadas: I (isort), F (flake8), E (pycodestyle), W (warning), PL (pylint), PT (pytest)
