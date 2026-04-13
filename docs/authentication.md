# Autenticação e Segurança

Este documento detalha o sistema de autenticação e segurança implementado na API.

## Visão Geral

O sistema utiliza **JWT (JSON Web Tokens)** para autenticação stateless, combinado com **Argon2** para hash de senhas e verificações de autorização baseadas em propriedade.

## Componentes de Segurança

### Hash de Senhas

As senhas são armazenadas utilizando **Argon2**, o algoritmo recomendado pela competição Password Hashing Competition.

**Localização:** `car_api/core/security.py`

```python
from pwdlib import PasswordHash

pwd_context = PasswordHash.recommended()

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
```

**Características do Argon2:**
- Resistente a ataques de GPU e ASIC
- Configurável em memória, tempo e paralelismo
- Considerado seguro para armazenamento de senhas

### JWT (JSON Web Tokens)

Tokens JWT são utilizados para autenticação stateless, permitindo que a API escale horizontalmente sem necessidade de sessão no servidor.

**Configurações:**

| Parâmetro | Valor Padrão | Descrição |
|-----------|--------------|-----------|
| `JWT_ALGORITHM` | `HS256` | Algoritmo de assinatura |
| `JWT_EXPIRATION_MINUTES` | `30` | Tempo de expiração em minutos |
| `JWT_SECRET_KEY` | (configurável) | Chave secreta para assinatura |

#### Geração de Token

```python
def create_access_token(data: Dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.JWT_EXPIRATION_MINUTES
    )
    to_encode.update({'exp': expire})
    
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt
```

**Payload do Token:**
```json
{
  "sub": "user_id",
  "exp": 1712937600
}
```

- `sub`: Identificador único do usuário
- `exp`: Timestamp de expiração (UTC)

#### Validação de Token

```python
def verify_token(token: str) -> Dict:
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='O token expirou',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Não foi possível validar as credenciais',
            headers={'WWW-Authenticate': 'Bearer'},
        )
```

## Fluxo de Autenticação

### 1. Login

```
POST /api/v1/auth/token
{
  "email": "usuario@email.com",
  "password": "senha123"
}
```

**Processo:**
1. Recebe e-mail e senha do usuário
2. Busca usuário no banco de dados pelo e-mail
3. Verifica senha com Argon2 (`verify_password`)
4. Se válido, gera JWT token com `sub=user_id`
5. Retorna token e tipo

**Respostas:**
- `200` - Token gerado com sucesso
- `401` - E-mail ou senha incorreto

### 2. Acesso a Rotas Protegidas

Todas as rotas protegidas utilizam o dependency `get_current_user`:

```python
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_session),
) -> User:
    payload = verify_token(credentials.credentials)
    user_id = int(payload.get('sub'))
    # Busca usuário no banco
    return user
```

**Processo:**
1. Extrai token do header `Authorization: Bearer <token>`
2. Decodifica e valida token (assinatura e expiração)
3. Extrai `user_id` do payload
4. Busca usuário no banco de dados
5. Retorna objeto User

**Respostas de Erro:**
- `401` - Token inválido ou expirado
- `401` - Usuário não encontrado no banco

### 3. Refresh de Token

```
POST /api/v1/auth/refresh_token
Authorization: Bearer <token_atual>
```

**Processo:**
1. Valida token atual via `get_current_user`
2. Gera novo token com mesmo `user_id`
3. Retorna novo token

**Respostas:**
- `200` - Novo token gerado
- `401` - Token atual inválido/expirado

## Autorização

### Controle de Acesso por Propriedade

Além da autenticação, o sistema implementa controle de acesso baseado em propriedade para operações com carros.

```python
def verify_car_ownership(user: User, car_owner_id: int) -> None:
    if user.id != car_owner_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Permissões insuficientes para acessar este carro',
        )
```

**Aplicação:**
- Usuários só podem **atualizar** seus próprios carros
- Usuários só podem **deletar** seus próprios carros
- Apenas o proprietário pode **transferir** um carro

**Endpoints com verificação de propriedade:**
- `PUT /api/v1/cars/{car_id}`
- `DELETE /api/v1/cars/{car_id}`
- `POST /api/v1/cars/{car_id}/transfer`

### Níveis de Acesso

| Recurso | Autenticado? | Proprietário? | Ação Permitida |
|---------|--------------|---------------|----------------|
| Listar carros | Sim | Não | ✅ Leitura |
| Criar carro | Sim | N/A | ✅ Criar |
| Ver carro | Sim | Não | ✅ Leitura |
| Atualizar carro | Sim | Sim | ✅ Atualizar |
| Atualizar carro | Sim | Não | ❌ 403 Forbidden |
| Deletar carro | Sim | Sim | ✅ Deletar |
| Deletar carro | Sim | Não | ❌ 403 Forbidden |
| Transferir carro | Sim | Sim | ✅ Transferir |
| Transferir carro | Sim | Não | ❌ 403 Forbidden |

## Boas Práticas de Segurança

### Senhas

- **Mínimo de 6 caracteres** (validado via Pydantic)
- **Hash com Argon2** (nunca armazenar senhas em texto puro)
- **Verificação segura** (prevenção contra timing attacks)

### Tokens

- **Expiração curta** (30 minutos por padrão)
- **Algoritmo forte** (HS256 mínimo)
- **Chave secreta forte** (gerar com `secrets.token_urlsafe(32)`)
- **HTTPS obrigatório em produção** (para evitar interception)

### Validação de Input

- **Pydantic schemas** para todos os endpoints
- **Validação de tipos** (int, str, email, decimal)
- **Validação de comprimento** (mínimo de caracteres)
- **Validação de formato** (placa de carro)
- **Validação de unicidade** (username, email, placa)

### Banco de Dados

- **Constraints de unicidade** (username, email, plate)
- **Foreign keys** (brand_id, owner_id)
- **Validação de integridade** (não deletar marca com carros)

## Recomendações para Produção

1. **HTTPS obrigatório** - Nunca utilize JWT sem HTTPS
2. **Rotação de chaves** - Altere `JWT_SECRET_KEY` periodicamente
3. **Tempo de expiração** - Reduza para 15 minutos em aplicações sensíveis
4. **Rate limiting** - Implemente limitação de requisições no endpoint de login
5. **Logging** - Registre falhas de autenticação para detecção de ataques
6. **CORS** - Configure origens permitidas explicitamente
7. **Backup de chaves** - Armazene `JWT_SECRET_KEY` em gerenciador de segredos (AWS Secrets Manager, HashiCorp Vault)

## Estrutura de Segurança

```
car_api/core/security.py
├── get_password_hash()      # Hash de senhas com Argon2
├── verify_password()        # Verificação de senhas
├── create_access_token()    # Geração de tokens JWT
├── verify_token()           # Validação de tokens
├── authenticate_user()      # Autenticação completa (email + senha)
├── get_current_user()       # Dependency para rotas protegidas
└── verify_car_ownership()   # Verificação de propriedade
```
