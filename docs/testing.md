# Testes

Este documento descreve a estratégia e execução de testes no projeto.

## Visão Geral

O projeto possui uma estrutura de testes organizada no diretório `tests/`. Embora os testes ainda estejam em fase inicial, a arquitetura está preparada para suportar testes unitários e de integração.

## Estrutura de Testes

```
tests/
├── __init__.py
├── conftest.py          # Fixtures e configurações compartilhadas (a criar)
├── test_auth.py         # Testes de autenticação (a criar)
├── test_users.py        # Testes de usuários (a criar)
├── test_brands.py       # Testes de marcas (a criar)
└── test_cars.py         # Testes de carros (a criar)
```

## Executando Testes

### Framework Recomendado: Pytest

O projeto está configurado para utilizar **pytest** como framework de testes.

**Executar todos os testes:**

```bash
poetry run pytest
```

**Executar com verbosity:**

```bash
poetry run pytest -v
```

**Executar arquivo específico:**

```bash
poetry run pytest tests/test_auth.py
```

**Executar teste específico:**

```bash
poetry run pytest tests/test_auth.py::test_token_success
```

**Executar com cobertura:**

```bash
poetry run pytest --cov=car_api --cov-report=html
```

## Configurando Ambiente de Testes

### Banco de Dados de Testes

Para testes de integração, utilize um banco de dados em memória:

```python
# tests/conftest.py
import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from car_api.models.base import Base

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest.fixture(scope="session")
def engine():
    return create_async_engine(TEST_DATABASE_URL)

@pytest.fixture(scope="session")
async def setup_db(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def db_session(engine, setup_db):
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session
```

### Cliente de Teste FastAPI

```python
# tests/conftest.py
from fastapi.testclient import TestClient
from car_api.app import app

@pytest.fixture
def client():
    return TestClient(app)
```

## Escrevendo Testes

### Testes de Unitários

Teste funções isoladas:

```python
# tests/test_security.py
from car_api.core.security import get_password_hash, verify_password

def test_password_hash():
    hashed = get_password_hash("senha123")
    assert hashed != "senha123"
    assert hashed.startswith("$argon2")

def test_verify_password_correct():
    hashed = get_password_hash("senha123")
    assert verify_password("senha123", hashed) is True

def test_verify_password_incorrect():
    hashed = get_password_hash("senha123")
    assert verify_password("senha_errada", hashed) is False
```

### Testes de Integração

Teste endpoints completos:

```python
# tests/test_auth.py
from fastapi.testclient import TestClient

def test_create_user(client: TestClient):
    response = client.post("/api/v1/users/", json={
        "username": "testuser",
        "email": "test@email.com",
        "password": "senha123"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert "password" not in data

def test_login_success(client: TestClient):
    # Primeiro cria usuário
    client.post("/api/v1/users/", json={
        "username": "testuser",
        "email": "test@email.com",
        "password": "senha123"
    })
    
    # Depois faz login
    response = client.post("/api/v1/auth/token", json={
        "email": "test@email.com",
        "password": "senha123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_wrong_password(client: TestClient):
    response = client.post("/api/v1/auth/token", json={
        "email": "wrong@email.com",
        "password": "senha_errada"
    })
    assert response.status_code == 401
```

### Testes com Autenticação

Para testar endpoints protegidos:

```python
def test_create_car_with_auth(client: TestClient):
    # Cria usuário e faz login
    client.post("/api/v1/users/", json={
        "username": "testuser",
        "email": "test@email.com",
        "password": "senha123"
    })
    
    response = client.post("/api/v1/auth/token", json={
        "email": "test@email.com",
        "password": "senha123"
    })
    token = response.json()["access_token"]
    
    # Cria carro com token
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/api/v1/cars/", json={
        "model": "Corolla",
        "factory_year": 2024,
        "model_year": 2025,
        "color": "Prata",
        "plate": "ABC1D23",
        "fuel_type": "flex",
        "transmission": "automatic",
        "price": 150000.00,
        "brand_id": 1
    }, headers=headers)
    
    assert response.status_code in [201, 400]  # 400 se marca não existe
```

## Cobertura de Testes

### Instalar pytest-cov

```bash
poetry add --group dev pytest-cov
```

### Executar com Cobertura

```bash
poetry run pytest --cov=car_api --cov-report=term-missing
```

**Relatório HTML:**

```bash
poetry run pytest --cov=car_api --cov-report=html
# Abrir htmlcov/index.html
```

## Boas Práticas

### Naming Conventions

- Arquivos: `test_<modulo>.py`
- Funções: `test_<funcionalidade>_<cenario>`

Exemplo:
```python
def test_create_user_duplicate_username():
def test_delete_car_not_found():
def test_token_expired_password():
```

### Arrange-Act-Assert

Estruture testes em três partes:

```python
def test_update_car():
    # Arrange
    user = create_test_user()
    car = create_test_car(owner=user)
    update_data = {"model": "Novo Modelo"}
    
    # Act
    response = client.put(f"/api/v1/cars/{car.id}", json=update_data)
    
    # Assert
    assert response.status_code == 200
    assert response.json()["model"] == "Novo Modelo"
```

### Fixtures

Utilize fixtures para dados comuns:

```python
@pytest.fixture
async def test_user(db_session):
    user = User(
        username="testuser",
        email="test@email.com",
        password=get_password_hash("senha123")
    )
    db_session.add(user)
    await db_session.commit()
    return user

@pytest.fixture
async def test_car(db_session, test_user):
    car = Car(
        model="Corolla",
        factory_year=2024,
        model_year=2025,
        color="Prata",
        plate="ABC1D23",
        fuel_type="flex",
        transmission="automatic",
        price=150000.00,
        brand_id=1,
        owner_id=test_user.id
    )
    db_session.add(car)
    await db_session.commit()
    return car
```

### Testar Casos de Erro

Não teste apenas cenários de sucesso:

```python
def test_create_user_duplicate_username():
    client.post("/api/v1/users/", json={
        "username": "testuser",
        "email": "test@email.com",
        "password": "senha123"
    })
    
    response = client.post("/api/v1/users/", json={
        "username": "testuser",  # mesmo username
        "email": "other@email.com",
        "password": "senha123"
    })
    
    assert response.status_code == 400
    assert "Username já está em uso" in response.json()["detail"]
```

## Integração Contínua (CI/CD)

Exemplo de workflow GitHub Actions:

```yaml
# .github/workflows/tests.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.13'
      
      - name: Install Poetry
        run: curl -sSL https://install.python-poetry.org | python3 -
      
      - name: Install dependencies
        run: poetry install
      
      - name: Run linter
        run: poetry run task lint
      
      - name: Run tests
        run: poetry run pytest --cov=car_api
```

## Recursos

- [Pytest Documentation](https://docs.pytest.org/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [SQLAlchemy Testing](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
