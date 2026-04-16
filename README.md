# Car API 🚗

Uma API moderna e robusta para gerenciamento de veículos, marcas e usuários, desenvolvida com **FastAPI** e conectada a um banco de dados **PostgreSQL**.

## 🚀 Sobre o Projeto

A **Car API** foi projetada para oferecer uma solução completa de catálogo de veículos, permitindo o cadastro de usuários, autenticação via JWT, gerenciamento de marcas e o controle total sobre a frota de carros (incluindo transferência de propriedade).

### Principais Tecnologias
- **FastAPI**: Framework web de alta performance.
- **PostgreSQL**: Banco de dados relacional robusto.
- **SQLAlchemy (Async)**: ORM para mapeamento objeto-relacional com suporte assíncrono.
- **Alembic**: Gerenciamento de migrações de banco de dados.
- **Pydantic**: Validação de dados e definições de esquemas.
- **JWT (JSON Web Tokens)**: Autenticação segura.
- **Poetry**: Gerenciamento de dependências e pacotes.

---

## 🛣️ Rotas da API

A API está organizada em módulos. A base de todas as rotas (exceto health check) é `/api/v1`.

### 🔐 Autenticação (`/auth`)
| Método | Rota | Nome/Descrição |
| :--- | :--- | :--- |
| `POST` | `/token` | **Gerar token de acesso**: Realiza o login e retorna o JWT. |
| `POST` | `/refresh_token` | **Atualizar token**: Gera um novo token a partir de um válido. |

### 👤 Usuários (`/users`)
| Método | Rota | Nome/Descrição |
| :--- | :--- | :--- |
| `POST` | `/` | **Criar novo usuário**: Registra um novo usuário no sistema. |
| `GET` | `/` | **Listar usuários**: Retorna a lista de usuários cadastrados. |
| `GET` | `/{user_id}` | **Buscar usuário por ID**: Detalhes de um usuário específico. |
| `PUT` | `/{user_id}` | **Atualizar usuário**: Modifica os dados do usuário logado. |
| `DELETE` | `/{user_id}` | **Deletar usuário**: Remove um usuário do sistema. |

### 🏷️ Marcas (`/brands`)
| Método | Rota | Nome/Descrição |
| :--- | :--- | :--- |
| `POST` | `/` | **Criar nova marca**: Cadastra uma fabricante de veículos. |
| `GET` | `/` | **Listar marcas**: Retorna as marcas com filtros de busca e status. |
| `GET` | `/{brand_id}` | **Buscar marca por ID**: Detalhes de uma marca específica. |
| `PUT` | `/{brand_id}` | **Atualizar marca**: Modifica os dados de uma marca existente. |
| `DELETE` | `/{brand_id}` | **Deletar marca**: Remove uma marca (se não houver carros associados). |

### 🏎️ Carros (`/cars`)
| Método | Rota | Nome/Descrição |
| :--- | :--- | :--- |
| `POST` | `/` | **Criar novo carro**: Registra um novo veículo no catálogo. |
| `GET` | `/` | **Listar carros**: Busca avançada de veículos com diversos filtros. |
| `GET` | `/{car_id}` | **Buscar carro por ID**: Detalhes completos de um veículo. |
| `PUT` | `/{car_id}` | **Atualizar carro**: Modifica os dados de um veículo (apenas o proprietário). |
| `DELETE` | `/{car_id}` | **Deletar carro**: Remove um veículo do sistema. |
| `POST` | `/{car_id}/transfer` | **Transferir carro**: Altera o proprietário de um veículo. |

### ⚙️ Geral
| Método | Rota | Nome/Descrição |
| :--- | :--- | :--- |
| `GET` | `/health_check` | **Health Check**: Verifica a integridade e status da API. |

---

## 🛠️ Como Executar

### Pré-requisitos
- Python 3.13+
- PostgreSQL
- Poetry

### Instalação
1. Clone o repositório.
2. Instale as dependências:
   ```bash
   poetry install
   ```
3. Configure as variáveis de ambiente no arquivo `.env` (use o `.env.example` como base).
4. Execute as migrações do banco de dados:
   ```bash
   poetry run alembic upgrade head
   ```

### Comandos Úteis (Taskipy)
O projeto utiliza o `taskipy` para facilitar a execução de comandos comuns:

- **Rodar a API**: `task run`
- **Rodar Testes**: `task test`
- **Formatação de Código**: `task format`
- **Linting**: `task lint`
- **Documentação (MkDocs)**: `task docs`

---

## 📖 Documentação Automática
Com a API rodando, você pode acessar a documentação interativa em:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
