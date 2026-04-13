# Desenvolvimento

Este guia fornece informações essenciais para desenvolvedores que desejam trabalhar no projeto.

## Ambiente de Desenvolvimento

### Editor Recomendado

- **VS Code** com extensões:
  - Python (Microsoft)
  - Ruff (charliermarsh)
  - SQLite Viewer
  - GitLens

### Configuração do VS Code

Crie `.vscode/settings.json`:

```json
{
  "python.defaultInterpreterPath": ".venv/bin/python",
  "python.linting.enabled": true,
  "python.linting.lintOnSave": true,
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff",
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.organizeImports": "explicit"
    }
  }
}
```

## Taskipy - Executor de Tarefas

O projeto utiliza Taskipy para executar comandos comuns. As tarefas estão definidas em `pyproject.toml`.

### Tarefas Disponíveis

| Tarefa | Comando | Descrição |
|--------|---------|-----------|
| `run` | `fastapi dev car_api/app.py` | Inicia servidor de desenvolvimento |
| `lint` | `ruff check` | Verifica erros de lint |
| `pre_format` | `ruff check --fix` | Corrige problemas de lint automaticamente |
| `format` | `ruff format` | Formata o código |
| `docs` | `mkdocs serve -a 127.0.0.1:8001` | Serve documentação localmente |

### Execução

```bash
# Iniciar servidor
poetry run task run

# Verificar lint
poetry run task lint

# Formatar código
poetry run task format

# Servir documentação
poetry run task docs
```

## Ruff - Linter e Formatter

### Configuração

Localizado em `pyproject.toml`:

```toml
[tool.ruff]
line-length = 79
exclude = ["alembic", "migrations", ...]

[tool.ruff.lint]
preview = true
select = ['I', 'F', 'E', 'W', 'PL', 'PT']
ignore = ['E501', 'PLR2004', 'PLR0917', 'PLR0913']

[tool.ruff.format]
preview = true
quote-style = 'single'
```

### Executar Manualmente

```bash
# Verificar erros
poetry run ruff check

# Corrigir automaticamente
poetry run ruff check --fix

# Formatar código
poetry run ruff format

# Verificar arquivo específico
poetry run ruff check car_api/core/security.py
```

## Desenvolvimento de Novos Endpoints

### Passo 1: Criar/Atualizar Model

Se necessário, crie ou modifique o modelo em `car_api/models/`:

```python
# car_api/models/example.py
from sqlalchemy.orm import Mapped, mapped_column

from car_api.models import Base

class Example(Base):
    __tablename__ = 'examples'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
```

Exporte o model em `car_api/models/__init__.py`:

```python
from car_api.models.example import Example

__all__ = ['Base', 'Brand', 'Car', 'User', 'Example']
```

### Passo 2: Criar Schema

Crie schemas de validação em `car_api/schemas/`:

```python
# car_api/schemas/example.py
from pydantic import BaseModel

class ExampleSchema(BaseModel):
    name: str

class ExamplePublicSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
```

### Passo 3: Criar Router

Crie endpoints em `car_api/routers/`:

```python
# car_api/routers/example.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from car_api.core.database import get_session
from car_api.schemas.example import ExampleSchema, ExamplePublicSchema

router = APIRouter()

@router.post(
    path='/',
    status_code=status.HTTP_201_CREATED,
    response_model=ExamplePublicSchema,
)
async def create_example(
    example: ExampleSchema,
    db: AsyncSession = Depends(get_session),
):
    ...
```

### Passo 4: Registrar Router no App

Adicione o router em `car_api/app.py`:

```python
from car_api.routers import example

app.include_router(
    router=example.router,
    prefix='/api/v1/examples',
    tags=['Examples'],
)
```

### Passo 5: Gerar Migração

```bash
poetry run alembic revision --autogenerate -m "create examples table"
poetry run alembic upgrade head
```

## Depuração

### FastAPI Auto-Reload

O servidor de desenvolvimento possui auto-reload ativado. Alterações no código recarregam automaticamente.

### Logs

Ative logs detalhados configurando o nível de log:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Swagger UI Interativo

Acesse `http://127.0.0.1:8000/docs` para:
- Testar endpoints manualmente
- Ver schemas de request/response
- Autenticar via interface gráfica

### ReDoc

Acesse `http://127.0.0.1:8000/redoc` para documentação alternativa.

## Banco de Dados

### Visualizar Dados

Utilize extensões VS Code como:
- SQLite Viewer
- SQLite3 Editor

Ou via linha de comando:

```bash
sqlite3 car_api.db
```

### Resetar Banco de Dados

ParaDevelopment, remova o banco e recrie:

```bash
rm car_api.db
poetry run alembic upgrade head
```

## Convenções de Código

- **Aspas simples** para strings
- **Type hints** em todas as funções
- **Async/await** para operações de I/O
- **Nomes em inglês** para arquivos e código
- **Documentação em pt-BR**

## Git Workflow

1. Crie uma branch para sua feature:
   ```bash
   git checkout -b feat/nome-da-feature
   ```

2. Faça commits frequentes e descritivos:
   ```bash
   git commit -m "feat: adicionar endpoint de transferência de carros"
   ```

3. Mantenha sua branch atualizada:
   ```bash
   git fetch origin
   git rebase origin/main
   ```

4. Execute lint e testes antes de push:
   ```bash
   poetry run task lint
   # Execute testes se existirem
   ```

## Performance

### Operações Assíncronas

Todas as operações de banco de dados são assíncronas:

```python
# ✅ Correto
result = await db.execute(select(User))
users = result.scalars().all()

# ❌ Incorreado (bloqueante)
users = db.query(User).all()
```

### Lazy Loading vs Eager Loading

Para evitar queries N+1, utilize `selectinload`:

```python
from sqlalchemy.orm import selectinload

result = await db.execute(
    select(Car)
    .options(selectinload(Car.brand), selectinload(Car.owner))
    .where(Car.id == car_id)
)
```

## Recursos Úteis

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Async Documentation](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
- [Pydantic V2 Documentation](https://docs.pydantic.dev/latest/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
