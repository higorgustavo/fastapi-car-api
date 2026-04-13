# Guidelines e Padrões

Este documento descreve as convenções e padrões adotados no projeto para garantir consistência, legibilidade e manutenibilidade do código.

## Estilo de Código

### Ruff

Utilizamos o [Ruff](https://docs.astral.sh/ruff/) como linter e formatador. As configurações estão em `pyproject.toml`.

**Regras Principais:**
- Comprimento máximo de linha: 79 caracteres
- Aspas simples (`'`) para strings
- Formatação automática com `poetry run task format`

**Executar linting:**
```bash
poetry run task lint
```

**Corrigir e formatar:**
```bash
poetry run task format
```

### Regras do Ruff Ativas

| Código | Descrição |
|--------|-----------|
| `I` | isort - Ordenação de imports |
| `F` | Pyflakes - Erros de lint |
| `E` | Pycodestyle Errors |
| `W` | Pycodestyle Warnings |
| `PL` | Pylint |
| `PT` | Flake8-pyteststyle |

**Regras Ignoradas:**
- `E501` - Line too long (controlado pelo formatter)
- `PLR2004` - Magic value comparison
- `PLR0917` - Too many positional arguments
- `PLR0913` - Too many arguments

## Python

### Type Hints

Utilize type hints em todas as funções e métodos:

```python
from typing import Optional

async def get_user(user_id: int, db: AsyncSession) -> Optional[User]:
    ...
```

### Nomenclatura

| Tipo | Convenção | Exemplo |
|------|-----------|---------|
| Classes | PascalCase | `UserSchema`, `Car` |
| Funções/Métodos | snake_case | `get_current_user`, `create_car` |
| Variáveis | snake_case | `user_id`, `access_token` |
| Constantes | UPPER_SNAKE_CASE | `DATABASE_URL`, `JWT_SECRET_KEY` |
| Enums | PascalCase | `FuelType`, `TransmissionType` |
| Arquivos | snake_case | `auth.py`, `cars.py` |

### Imports

Ordene os imports seguindo a convenção isort:

1. Standard library
2. Third-party packages
3. Local application imports

```python
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from car_api.core.database import get_session
from car_api.models.users import User
```

### Async/Await

Todas as operações de I/O devem ser assíncronas:

```python
async def list_users(
    db: AsyncSession = Depends(get_session),
):
    result = await db.execute(select(User))
    return result.scalars().all()
```

## FastAPI

### Routers

- Cada domínio possui seu próprio router (`auth.py`, `users.py`, `cars.py`, `brands.py`)
- Utilize `APIRouter()` para organizar endpoints
- Defina `prefix` e `tags` ao incluir o router no app

### Endpoints

**Estrutura padrão:**

```python
@router.post(
    path='/',
    status_code=status.HTTP_201_CREATED,
    response_model=UserPublicSchema,
    summary='Criar novo usuário',
)
async def create_user(
    user: UserSchema,
    db: AsyncSession = Depends(get_session),
):
    ...
```

**Convenções:**
- Utilize `status_code` explícito
- Defina `response_model` para documentação automática
- Adicione `summary` descritivo
- Use `Depends` para injeção de dependências

### Schemas (Pydantic)

**Separação de responsabilidades:**

| Schema | Uso |
|--------|-----|
| `*Schema` | Entrada de dados (criação) |
| `*UpdateSchema` | Atualização parcial (campos opcionais) |
| `*PublicSchema` | Resposta pública (sem dados sensíveis) |
| `*ListPublicSchema` | Respostas de listagem com paginação |

**Validações com Field Validators:**

```python
@field_validator('password')
def password_min_length(cls, v):
    if len(v) < 6:
        raise ValueError('Senha deve ter pelo menos 2 caracteres')
    return v
```

### Tratamento de Erros

Utilize `HTTPException` com códigos de status apropriados:

```python
raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='Usuário não encontrado',
)
```

**Códigos de Status:**

| Código | Uso |
|--------|-----|
| `200 OK` | GET, PUT bem-sucedidos |
| `201 Created` | POST bem-sucedido |
| `204 No Content` | DELETE bem-sucedido |
| `400 Bad Request` | Validação falhou |
| `401 Unauthorized` | Token inválido/expirado |
| `403 Forbidden` | Permissões insuficientes |
| `404 Not Found` | Recurso não encontrado |

## SQLAlchemy

### Models

- Herde de `Base` (DeclarativeBase)
- Utilize `Mapped` e `mapped_column` para tipagem moderna
- Defina `__tablename__` no plural

```python
class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
```

### Relacionamentos

Utilize `relationship` com `back_populates`:

```python
class User(Base):
    cars: Mapped[List['Car']] = relationship(
        back_populates='owner',
    )
```

### Timestamps

Sempre inclua `created_at` e `updated_at`:

```python
created_at: Mapped[datetime] = mapped_column(server_default=func.now())
updated_at: Mapped[datetime] = mapped_column(
    onupdate=func.now(),
    server_default=func.now(),
)
```

## Git

### Commits

Siga o padrão de mensagens concisas e descritivas:

```
<tipo>: <descrição curta>

<corpo opcional explicando o porquê>
```

**Tipos comuns:**
- `feat`: Nova funcionalidade
- `fix`: Correção de bug
- `docs`: Alterações na documentação
- `style`: Formatação, sem alteração lógica
- `refactor`: Refatoração de código
- `test`: Adição ou correção de testes
- `chore`: Atualizações de build/dependências

### Branches

- `main` - Branch principal com código estável
- `feat/<nome>` - Features novas
- `fix/<nome>` - Correções
- `docs/<nome>` - Alterações na documentação

## Documentação

- Documentação em **português brasileiro (pt-BR)**
- Nomes de arquivos `.md` em **inglês**
- Utilize Mermaid para diagramas
- Código de exemplos sempre testável
