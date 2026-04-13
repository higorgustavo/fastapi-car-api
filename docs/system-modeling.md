# Modelagem do Sistema

Esta seção apresenta os diagramas e modelos de dados do sistema utilizando Mermaid.

## Modelos de Dados (ERD)

O diagrama de entidade-relacionamento abaixo mostra os modelos do banco de dados e seus relacionamentos:

```mermaid
erDiagram
    users {
        int id PK
        string username UK
        string password
        string email UK
        datetime created_at
        datetime updated_at
    }

    brands {
        int id PK
        string name UK
        bool is_active
        text description
        datetime created_at
        datetime updated_at
    }

    cars {
        int id PK
        string model
        int factory_year
        int model_year
        string color
        string plate UK
        string fuel_type
        string transmission
        decimal price
        text description
        bool is_available
        int brand_id FK
        int owner_id FK
        datetime created_at
        datetime updated_at
    }

    users ||--o{ cars : "owns"
    brands ||--o{ cars : "has"
```

### Relacionamentos

| Relação | Tipo | Descrição |
|---------|------|-----------|
| `users` → `cars` | 1:N | Um usuário pode possuir vários carros |
| `brands` → `cars` | 1:N | Uma marca pode ter vários carros |
| `cars` → `users` | N:1 | Cada carro pertence a um único usuário |
| `cars` → `brands` | N:1 | Cada carro pertence a uma única marca |

### Enums

**FuelType (fuel_type):**
- `gasoline` - Gasolina
- `ethanol` - Etanol
- `flex` - Flex
- `diesel` - Diesel
- `electric` - Elétrico
- `hybrid` - Híbrido

**TransmissionType (transmission):**
- `manual` - Manual
- `automatic` - Automática
- `semi_automatic` - Semi-automática
- `cvt` - CVT

---

## Arquitetura do Sistema

A arquitetura do sistema segue o padrão REST com camadas bem definidas:

```mermaid
graph TB
    subgraph Cliente
        A[Cliente HTTP]
    end

    subgraph "FastAPI Application"
        B[App - car_api/app.py]
        
        subgraph Routers
            C1[auth.py]
            C2[users.py]
            C3[brands.py]
            C4[cars.py]
        end
        
        subgraph Schemas
            D1[auth.py]
            D2[users.py]
            D3[brands.py]
            D4[cars.py]
        end
        
        subgraph Core
            E1[database.py]
            E2[security.py]
            E3[settings.py]
        end
        
        subgraph Models
            F1[users.py]
            F2[cars.py]
            F3[base.py]
        end
    end

    subgraph "Camada de Dados"
        G[(SQLite/PostgreSQL)]
    end

    A -->|HTTP Request| B
    B --> C1
    B --> C2
    B --> C3
    B --> C4
    
    C1 -.->|Validação| D1
    C2 -.->|Validação| D2
    C3 -.->|Validação| D3
    C4 -.->|Validação| D4
    
    C1 -->|Autenticação| E2
    C2 -->|Auth| E2
    C3 -->|Auth| E2
    C4 -->|Auth| E2
    
    C1 -->|Session| E1
    C2 -->|Session| E1
    C3 -->|Session| E1
    C4 -->|Session| E1
    
    E1 -->|Config| E3
    E2 -->|Config| E3
    
    E1 -->|ORM| F1
    E1 -->|ORM| F2
    E1 -->|ORM| F3
    
    E1 -->|Async I/O| G
    
    F1 -.->|Herda| F3
    F2 -.->|Herda| F3
```

### Fluxo de Requisição

1. **Cliente** envia requisição HTTP
2. **App** roteia para o **Router** correspondente
3. **Router** valida dados de entrada com **Schemas** (Pydantic)
4. **Router** verifica autenticação via **Security**
5. **Router** obtém sessão do banco via **Database**
6. **Database** executa operações com **Models** (SQLAlchemy ORM)
7. **Router** retorna resposta serializada via **Schemas**

---

## Fluxo de Autenticação

O fluxo de autenticação utiliza tokens JWT (JSON Web Tokens):

```mermaid
sequenceDiagram
    participant Client as Cliente
    participant Auth as Auth Router
    participant Security as Security Module
    participant DB as Database

    Client->>Auth: POST /auth/token (email, password)
    Auth->>DB: SELECT * FROM users WHERE email = ?
    DB-->>Auth: User (ou null)
    
    alt Usuário não encontrado
        Auth-->>Client: 401 Unauthorized
    else Senha incorreta
        Auth-->>Client: 401 Unauthorized
    else Autenticação bem-sucedida
        Auth->>Security: create_access_token(user.id)
        Security-->>Auth: JWT Token
        Auth-->>Client: 200 OK {access_token, token_type}
    end

    Note over Client,DB: Requisições Protegidas
    
    Client->>Auth: GET /cars (Authorization: Bearer <token>)
    Auth->>Security: get_current_user(token)
    Security->>Security: verify_token(token)
    
    alt Token inválido/expirado
        Security-->>Auth: HTTPException 401
        Auth-->>Client: 401 Unauthorized
    else Token válido
        Security->>DB: SELECT * FROM users WHERE id = ?
        DB-->>Security: User
        Security-->>Auth: User (autenticado)
        Auth->>DB: Query de carros
        DB-->>Auth: Cars
        Auth-->>Client: 200 OK {cars}
    end

    Note over Client,DB: Refresh de Token
    
    Client->>Auth: POST /auth/refresh_token (Bearer <token>)
    Auth->>Security: get_current_user(token)
    Security-->>Auth: User autenticado
    Auth->>Security: create_access_token(user.id)
    Security-->>Auth: Novo JWT Token
    Auth-->>Client: 200 OK {novo_access_token}
```

### Características do Token

- **Algoritmo**: HS256 (HMAC-SHA256)
- **Payload**: `{sub: user_id, exp: expiration_time}`
- **Expiração padrão**: 30 minutos
- **Transporte**: Header `Authorization: Bearer <token>`

---

## Fluxo CRUD de Carros

O ciclo de vida completo de operações com carros:

```mermaid
sequenceDiagram
    participant Client as Cliente (Autenticado)
    participant Router as Cars Router
    participant Security as Security Module
    participant DB as Database

    Note over Client,DB: CREATE - Criar Carro
    
    Client->>Router: POST /cars {car_data}
    Router->>Security: get_current_user(token)
    Security-->>Router: User autenticado
    
    Router->>DB: Verificar plate existente
    alt Placa já existe
        DB-->>Router: True
        Router-->>Client: 400 Bad Request
    else Placa disponível
        DB-->>Router: False
        Router->>DB: Verificar brand_id existe
        alt Marca não existe
            DB-->>Router: False
            Router-->>Client: 400 Bad Request
        else Marca existe
            DB-->>Router: True
            Router->>DB: INSERT INTO cars (owner_id = user.id)
            DB-->>Router: Car criado
            Router-->>Client: 201 Created {car}
        end
    end

    Note over Client,DB: READ - Listar/Buscar Carros
    
    Client->>Router: GET /cars?search=corolla&brand_id=1
    Router->>Security: get_current_user(token)
    Security-->>Router: User autenticado
    Router->>DB: SELECT cars WHERE filters
    DB-->>Router: Lista de carros
    Router-->>Client: 200 OK {cars, offset, limit}

    Note over Client,DB: UPDATE - Atualizar Carro
    
    Client->>Router: PUT /cars/{id} {update_data}
    Router->>Security: get_current_user(token)
    Security-->>Router: User autenticado
    Router->>DB: SELECT car WHERE id = ?
    
    alt Carro não existe
        DB-->>Router: Null
        Router-->>Client: 404 Not Found
    else Carro existe
        DB-->>Router: Car
        Router->>Router: verify_car_ownership(user, car.owner_id)
        
        alt Não é proprietário
            Router-->>Client: 403 Forbidden
        else É proprietário
            Router->>DB: UPDATE cars SET ...
            DB-->>Router: Car atualizado
            Router-->>Client: 200 OK {car}
        end
    end

    Note over Client,DB: DELETE - Deletar Carro
    
    Client->>Router: DELETE /cars/{id}
    Router->>Security: get_current_user(token)
    Security-->>Router: User autenticado
    Router->>DB: SELECT car WHERE id = ?
    Router->>Router: verify_car_ownership(user, car.owner_id)
    
    alt Não é proprietário
        Router-->>Client: 403 Forbidden
    else É proprietário
        Router->>DB: DELETE FROM cars WHERE id = ?
        DB-->>Router: Sucesso
        Router-->>Client: 204 No Content
    end

    Note over Client,DB: TRANSFER - Transferir Carro
    
    Client->>Router: POST /cars/{id}/transfer {new_owner_id}
    Router->>Security: get_current_user(token)
    Security-->>Router: User autenticado (atual)
    Router->>DB: SELECT car WHERE id = ?
    Router->>Router: verify_car_ownership(user, car.owner_id)
    
    alt Não é proprietário
        Router-->>Client: 403 Forbidden
    else É proprietário
        Router->>DB: SELECT user WHERE id = new_owner_id
        
        alt Novo proprietário não existe
            DB-->>Router: Null
            Router-->>Client: 404 Not Found
        else Novo proprietário existe
            DB-->>Router: New Owner
            Router->>DB: UPDATE cars SET owner_id = new_owner_id
            DB-->>Router: Sucesso
            Router-->>Client: 200 OK {car com novo owner}
        end
    end
```

---

## Fluxo de Segurança

O sistema de segurança abrange autenticação, autorização e validação de propriedade:

```mermaid
flowchart TD
    A[Requisição HTTP] --> B{Endpoint protegido?}
    
    B -->|Não| C[Processar normalmente]
    B -->|Sim| D[Extrair token do header]
    
    D --> E{Token presente?}
    E -->|Não| F[401 Unauthorized]
    E -->|Sim| G[verify_token]
    
    G --> H{Token válido?}
    H -->|Expirado| I[401 - Token expirou]
    H -->|Inválido| J[401 - Não foi possível validar]
    H -->|Válido| K[Extrair user_id do payload]
    
    K --> L[Buscar usuário no banco]
    L --> M{Usuário existe?}
    M -->|Não| N[401 Unauthorized]
    M -->|Sim| O[Retornar User object]
    
    O --> P[Prosseguir com handler]
    
    P --> Q{Operação em carro?}
    Q -->|Não| R[Executar operação]
    Q -->|Sim| S{É o proprietário?}
    
    S -->|Sim| R
    S -->|Não| T[403 Forbidden - Permissões insuficientes]
    
    C --> U[Resposta HTTP]
    R --> U
    F --> U
    I --> U
    J --> U
    N --> U
    T --> U
    
    style A fill:#e1f5fe
    style U fill:#c8e6c9
    style F fill:#ffcdd2
    style I fill:#ffcdd2
    style J fill:#ffcdd2
    style N fill:#ffcdd2
    style T fill:#ffcdd2
```

### Camadas de Segurança

| Camada | Mecanismo | Descrição |
|--------|-----------|-----------|
| **Autenticação** | JWT Bearer Token | Verifica identidade do usuário |
| **Validação de Token** | PyJWT + HS256 | Garante integridade e expiração |
| **Autorização** | `get_current_user` | Verifica existência do usuário |
| **Propriedade** | `verify_car_ownership` | Garante acesso apenas a recursos próprios |
| **Validação de Input** | Pydantic Schemas | Previne dados malformados |
| **Hash de Senha** | Argon2 (via pwdlib) | Armazenamento seguro de senhas |
| **Unicidade** | DB Constraints | Prev duplicatas de username, email, placa |
