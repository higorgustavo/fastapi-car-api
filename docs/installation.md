# Instalação

Siga os passos abaixo para instalar e configurar o projeto em seu ambiente local.

## Passo 1: Clonar o Repositório

```bash
git clone <url-do-repositorio>
cd car_api
```

## Passo 2: Instalar Dependências

O Poetry gerencia automaticamente o ambiente virtual e as dependências:

```bash
poetry install
```

Este comando irá:
- Criar um ambiente virtual isolado
- Instalar todas as dependências de produção e desenvolvimento
- Configurar o projeto em modo editável

### Dependências Instaladas

**Produção:**
- `fastapi[standard]` - Framework web
- `pydantic` - Validação de dados
- `sqlalchemy[asyncio]` - ORM assíncrono
- `aiosqlite` - Driver SQLite assíncrono
- `pydantic-settings` - Configuração via variáveis de ambiente
- `alembic` - Migrações de banco de dados
- `pwdlib[argon2]` - Hash de senhas
- `pyjwt` - Tokens JWT
- `mkdocs`, `mkdocs-material`, `pymdown-extensions` - Documentação

**Desenvolvimento:**
- `ruff` - Linter e formatador
- `taskipy` - Executor de tarefas

## Passo 3: Ativar o Ambiente Virtual (Opcional)

Para ativar manualmente o ambiente virtual:

```bash
poetry shell
```

Ou execute comandos dentro do ambiente:

```bash
poetry run <comando>
```

## Passo 4: Configurar Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas configurações:

```env
DATABASE_URL=sqlite+aiosqlite:///./car_api.db
JWT_SECRET_KEY=sua_chave_secreta_muito_segura_aqui
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=30
```

> **Atenção**: Nunca commite o arquivo `.env` no repositório. Ele já está listado no `.gitignore`.

## Passo 5: Executar Migrações

Crie o banco de dados e aplique as migrações:

```bash
poetry run alembic upgrade head
```

## Passo 6: Iniciar o Servidor

Inicie o servidor de desenvolvimento:

```bash
poetry run task run
```

O servidor estará disponível em `http://127.0.0.1:8000`.

## Verificação

Acesse a documentação interativa para verificar se a API está funcionando:

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc
- **Health Check**: http://127.0.0.1:8000/health_check

## Comandos Úteis

Todos os comandos disponíveis via Taskipy:

```bash
# Executar o servidor
poetry run task run

# Rodar o linter
poetry run task lint

# Formatar o código
poetry run task format

# Servir a documentação
poetry run task docs
```
