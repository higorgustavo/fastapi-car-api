# API Endpoints

Este documento descreve todos os endpoints disponíveis na API.

**URL Base:** `http://127.0.0.1:8000/api/v1`

> **Nota**: Todos os endpoints protegidos requerem autenticação via token JWT no header `Authorization: Bearer <token>`.

---

## Health Check

### `GET /health_check`

Verifica se a API está funcionando.

**Resposta:**
```json
{
  "status": "ok"
}
```

---

## Autenticação

### `POST /api/v1/auth/token`

Gera um token de acesso JWT.

**Corpo da Requisição:**
```json
{
  "email": "usuario@email.com",
  "password": "senha123"
}
```

**Resposta (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

**Respostas de Erro:**
- `401` - E-mail ou senha incorreto

---

### `POST /api/v1/auth/refresh_token`

Atualiza o token de acesso (requer autenticação).

**Headers:**
```
Authorization: Bearer <token_atual>
```

**Resposta (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

**Respostas de Erro:**
- `401` - Token inválido ou expirado

---

## Usuários

### `POST /api/v1/users/`

Cria um novo usuário.

**Corpo da Requisição:**
```json
{
  "username": "joaosilva",
  "email": "joao@email.com",
  "password": "senha123"
}
```

**Validações:**
- `username`: mínimo 3 caracteres, deve ser único
- `email`: formato válido, deve ser único
- `password`: mínimo 6 caracteres

**Resposta (201):**
```json
{
  "id": 1,
  "username": "joaosilva",
  "email": "joao@email.com",
  "created_at": "2026-04-12T10:00:00",
  "updated_at": "2026-04-12T10:00:00"
}
```

**Respostas de Erro:**
- `400` - Username ou e-mail já está em uso

---

### `GET /api/v1/users/`

Lista usuários com paginação e busca.

**Parâmetros de Query:**
| Parâmetro | Tipo | Padrão | Descrição |
|-----------|------|--------|-----------|
| `offset` | int | 0 | Registros para pular (≥ 0) |
| `limit` | int | 100 | Limite de registros (1-100) |
| `search` | string | null | Busca por username ou email |

**Exemplo:**
```
GET /api/v1/users/?offset=0&limit=10&search=joao
```

**Resposta (200):**
```json
{
  "users": [
    {
      "id": 1,
      "username": "joaosilva",
      "email": "joao@email.com",
      "created_at": "2026-04-12T10:00:00",
      "updated_at": "2026-04-12T10:00:00"
    }
  ],
  "offset": 0,
  "limit": 10
}
```

---

### `GET /api/v1/users/{user_id}`

Busca um usuário específico por ID.

**Resposta (200):**
```json
{
  "id": 1,
  "username": "joaosilva",
  "email": "joao@email.com",
  "created_at": "2026-04-12T10:00:00",
  "updated_at": "2026-04-12T10:00:00"
}
```

**Respostas de Erro:**
- `404` - Usuário não encontrado

---

### `PUT /api/v1/users/{user_id}`

Atualiza um usuário (requer autenticação).

**Headers:**
```
Authorization: Bearer <token>
```

**Corpo da Requisição (campos opcionais):**
```json
{
  "username": "novo_username",
  "email": "novo@email.com",
  "password": "nova_senha"
}
```

**Resposta (201):**
```json
{
  "id": 1,
  "username": "novo_username",
  "email": "novo@email.com",
  "created_at": "2026-04-12T10:00:00",
  "updated_at": "2026-04-12T11:00:00"
}
```

**Respostas de Erro:**
- `400` - Username ou email já está em uso
- `401` - Token inválido
- `404` - Usuário não encontrado

---

### `DELETE /api/v1/users/{user_id}`

Deleta um usuário (requer autenticação).

**Headers:**
```
Authorization: Bearer <token>
```

**Resposta:** `204 No Content`

**Respostas de Erro:**
- `401` - Token inválido
- `404` - Usuário não encontrado

---

## Marcas

### `POST /api/v1/brands/`

Cria uma nova marca (requer autenticação).

**Headers:**
```
Authorization: Bearer <token>
```

**Corpo da Requisição:**
```json
{
  "name": "Toyota",
  "description": "Marca japonesa de veículos",
  "is_active": true
}
```

**Validações:**
- `name`: mínimo 2 caracteres, deve ser único

**Resposta (201):**
```json
{
  "id": 1,
  "name": "Toyota",
  "description": "Marca japonesa de veículos",
  "is_active": true,
  "created_at": "2026-04-12T10:00:00",
  "updated_at": "2026-04-12T10:00:00"
}
```

**Respostas de Erro:**
- `400` - Nome da marca já está em uso
- `401` - Token inválido

---

### `GET /api/v1/brands/`

Lista marcas com paginação e filtros.

**Parâmetros de Query:**
| Parâmetro | Tipo | Padrão | Descrição |
|-----------|------|--------|-----------|
| `offset` | int | 0 | Registros para pular (≥ 0) |
| `limit` | int | 100 | Limite de registros (1-100) |
| `search` | string | null | Busca por nome |
| `is_active` | bool | null | Filtrar por marcas ativas |

**Resposta (200):**
```json
{
  "brands": [
    {
      "id": 1,
      "name": "Toyota",
      "description": "Marca japonesa de veículos",
      "is_active": true,
      "created_at": "2026-04-12T10:00:00",
      "updated_at": "2026-04-12T10:00:00"
    }
  ],
  "offset": 0,
  "limit": 100
}
```

---

### `GET /api/v1/brands/{brand_id}`

Busca uma marca específica por ID.

**Resposta (200):**
```json
{
  "id": 1,
  "name": "Toyota",
  "description": "Marca japonesa de veículos",
  "is_active": true,
  "created_at": "2026-04-12T10:00:00",
  "updated_at": "2026-04-12T10:00:00"
}
```

**Respostas de Erro:**
- `404` - Marca não encontrada

---

### `PUT /api/v1/brands/{brand_id}`

Atualiza uma marca (requer autenticação).

**Corpo da Requisição (campos opcionais):**
```json
{
  "name": "Toyota Motors",
  "description": "Nova descrição",
  "is_active": false
}
```

**Resposta (200):**
```json
{
  "id": 1,
  "name": "Toyota Motors",
  "description": "Nova descrição",
  "is_active": false,
  "created_at": "2026-04-12T10:00:00",
  "updated_at": "2026-04-12T11:00:00"
}
```

**Respostas de Erro:**
- `400` - Nome da marca já está em uso
- `401` - Token inválido
- `404` - Marca não encontrada

---

### `DELETE /api/v1/brands/{brand_id}`

Deleta uma marca (requer autenticação).

**Resposta:** `204 No Content`

**Respostas de Erro:**
- `400` - Não é possível deletar marca que possui carros associados
- `401` - Token inválido
- `404` - Marca não encontrada

---

## Carros

### `POST /api/v1/cars/`

Cria um novo carro (requer autenticação).

**Headers:**
```
Authorization: Bearer <token>
```

**Corpo da Requisição:**
```json
{
  "model": "Corolla",
  "factory_year": 2024,
  "model_year": 2025,
  "color": "Prata",
  "plate": "ABC1D23",
  "fuel_type": "flex",
  "transmission": "automatic",
  "price": 150000.00,
  "description": "Carro em excelente estado",
  "is_available": true,
  "brand_id": 1
}
```

**Enumerações:**

**fuel_type:**
| Valor | Descrição |
|-------|-----------|
| `gasoline` | Gasolina |
| `ethanol` | Etanol |
| `flex` | Flex |
| `diesel` | Diesel |
| `electric` | Elétrico |
| `hybrid` | Híbrido |

**transmission:**
| Valor | Descrição |
|-------|-----------|
| `manual` | Manual |
| `automatic` | Automática |
| `semi_automatic` | Semi-automática |
| `cvt` | CVT |

**Resposta (201):**
```json
{
  "id": 1,
  "model": "Corolla",
  "factory_year": 2024,
  "model_year": 2025,
  "color": "Prata",
  "plate": "ABC1D23",
  "fuel_type": "flex",
  "transmission": "automatic",
  "price": 150000.00,
  "description": "Carro em excelente estado",
  "is_available": true,
  "brand_id": 1,
  "owner_id": 1,
  "created_at": "2026-04-12T10:00:00",
  "updated_at": "2026-04-12T10:00:00",
  "brand": {
    "id": 1,
    "name": "Toyota",
    "description": "Marca japonesa de veículos",
    "is_active": true,
    "created_at": "2026-04-12T10:00:00",
    "updated_at": "2026-04-12T10:00:00"
  },
  "owner": {
    "id": 1,
    "username": "joaosilva",
    "email": "joao@email.com",
    "created_at": "2026-04-12T10:00:00",
    "updated_at": "2026-04-12T10:00:00"
  }
}
```

**Respostas de Erro:**
- `400` - Placa já está em uso / Marca não encontrada
- `401` - Token inválido

---

### `GET /api/v1/cars/`

Lista carros com paginação e filtros avançados.

**Parâmetros de Query:**
| Parâmetro | Tipo | Padrão | Descrição |
|-----------|------|--------|-----------|
| `offset` | int | 0 | Registros para pular (≥ 0) |
| `limit` | int | 100 | Limite de registros (1-100) |
| `search` | string | null | Busca por modelo, cor ou placa |
| `brand_id` | int | null | Filtrar por marca |
| `owner_id` | int | null | Filtrar por proprietário |
| `fuel_type` | enum | null | Filtrar por combustível |
| `transmission` | enum | null | Filtrar por transmissão |
| `is_available` | bool | null | Filtrar por disponibilidade |
| `min_price` | float | null | Preço mínimo |
| `max_price` | float | null | Preço máximo |

**Exemplo:**
```
GET /api/v1/cars/?brand_id=1&fuel_type=flex&min_price=100000&max_price=200000
```

**Resposta (200):**
```json
{
  "cars": [...],
  "offset": 0,
  "limit": 100
}
```

---

### `GET /api/v1/cars/{car_id}`

Busca um carro específico por ID.

**Resposta (200):** Mesma estrutura do POST.

**Respostas de Erro:**
- `401` - Token inválido
- `404` - Carro não encontrado

---

### `PUT /api/v1/cars/{car_id}`

Atualiza um carro (requer autenticação e propriedade).

**Headers:**
```
Authorization: Bearer <token>
```

**Corpo da Requisição (campos opcionais):**
```json
{
  "model": "Corolla XEi",
  "price": 160000.00,
  "is_available": false
}
```

**Resposta (200):** Objeto carro atualizado completo.

**Respostas de Erro:**
- `400` - Placa já está em uso / Marca não encontrada
- `401` - Token inválido
- `403` - Permissões insuficientes (não é o proprietário)
- `404` - Carro não encontrado

---

### `DELETE /api/v1/cars/{car_id}`

Deleta um carro (requer autenticação e propriedade).

**Headers:**
```
Authorization: Bearer <token>
```

**Resposta:** `204 No Content`

**Respostas de Erro:**
- `401` - Token inválido
- `403` - Permissões insuficientes
- `404` - Carro não encontrado

---

### `POST /api/v1/cars/{car_id}/transfer`

Transfere um carro para outro usuário (requer autenticação e propriedade).

**Headers:**
```
Authorization: Bearer <token>
```

**Corpo da Requisição:**
```json
{
  "new_owner_id": 2
}
```

**Resposta (200):** Objeto carro com novo proprietário.

**Respostas de Erro:**
- `401` - Token inválido
- `403` - Permissões insuficientes
- `404` - Carro ou novo proprietário não encontrado
