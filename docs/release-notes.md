# Release Notes

Histórico de versões e mudanças do projeto Car API.

---

## [0.1.0] - 2026-04-12

Versão inicial do Car API com funcionalidades básicas de gerenciamento de carros, marcas e usuários.

### Funcionalidades

#### Autenticação
- ✅ Geração de tokens JWT via `POST /api/v1/auth/token`
- ✅ Refresh de tokens via `POST /api/v1/auth/refresh_token`
- ✅ Autenticação baseada em email e senha
- ✅ Hash de senhas com Argon2
- ✅ Proteção de rotas via Bearer Token

#### Usuários
- ✅ Criação de usuários com validação completa
- ✅ Listagem com paginação e busca por username/email
- ✅ Busca individual por ID
- ✅ Atualização parcial de dados
- ✅ Remoção de usuários
- ✅ Validação de unicidade (username, email)

#### Marcas
- ✅ Criação de marcas
- ✅ Listagem com filtros (ativa/inativa) e busca
- ✅ Busca por ID
- ✅ Atualização de marcas
- ✅ Remoção com validação de dependência (não permite deletar marca com carros)

#### Carros
- ✅ Criação de carros com dados completos
  - Modelo, ano de fabricação, ano do modelo
  - Cor, placa, tipo de combustível, transmissão
  - Preço, descrição, disponibilidade
  - Vínculo com marca e proprietário
- ✅ Listagem com filtros avançados:
  - Busca por modelo, cor ou placa
  - Filtro por marca, proprietário
  - Filtro por tipo de combustível, transmissão
  - Filtro por disponibilidade
  - Filtro por faixa de preço (min/max)
- ✅ Busca individual por ID
- ✅ Atualização parcial ou total
- ✅ Remoção com verificação de propriedade
- ✅ Transferência de propriedade entre usuários

### Validações

#### Usuários
- Username: mínimo 3 caracteres
- Email: formato válido (EmailStr)
- Senha: mínimo 6 caracteres

#### Carros
- Modelo: mínimo 2 caracteres
- Cor: mínimo 2 caracteres
- Placa: entre 7 e 10 caracteres
- Ano: entre 1900 e 2030
- Preço: maior que zero

#### Marcas
- Nome: mínimo 2 caracteres

### Segurança
- ✅ Tokens JWT com expiração configurável
- ✅ Verificação de propriedade para operações em carros
- ✅ Validação rigorosa de inputs via Pydantic
- ✅ Constraints de unicidade no banco de dados

### Arquitetura
- ✅ FastAPI com suporte assíncrono completo
- ✅ SQLAlchemy Async para operações de banco não-bloqueantes
- ✅ Aiosqlite como driver de banco de dados
- ✅ Alembic para migrações
- ✅ Estrutura modular (core, models, routers, schemas)
- ✅ Pydantic v2 para validação de dados

### Desenvolvimento
- ✅ Ruff configurado como linter e formatter
- ✅ Taskipy para automação de tarefas
- ✅ Poetry para gerenciamento de dependências
- ✅ MkDocs + Material para documentação
- ✅ Servidor de desenvolvimento com auto-reload

### Banco de Dados
- ✅ Models com SQLAlchemy 2.0 (Mapped, mapped_column)
- ✅ Relacionamentos bidirecionais (back_populates)
- ✅ Timestamps automáticos (created_at, updated_at)
- ✅ Enums para fuel_type e transmission
- ✅ Foreign keys e constraints de unicidade

### Documentação
- ✅ Documentação completa em pt-BR
- ✅ Swagger UI interativa (/docs)
- ✅ ReDoc alternativa (/redoc)
- ✅ MkDocs com tema Material
- ✅ Diagramas Mermaid (ERD, arquitetura, fluxos)

### Conhecido
- ⚠️ Testes automatizados ainda não implementados
- ⚠️ Verificação de propriedade de carros comentada em alguns endpoints (listagem e busca)
- ⚠️ Validação de owner_id comentada na criação de carros (owner é sempre o usuário logado)
- ⚠️ Sem rate limiting no endpoint de login
- ⚠️ Sem paginação configurável por query parameter (offset/limit fixos)
- ⚠️ SQLite como único banco (migração para PostgreSQL necessária para produção)

---

## Formato de Versões

O projeto segue [Semantic Versioning](https://semver.org/lang/pt-BR/):

- **MAJOR** - Mudanças incompatíveis na API
- **MINOR** - Funcionalidades novas compatíveis
- **PATCH** - Correções de bugs compatíveis

### Template para Futuras Versões

```markdown
## [X.Y.Z] - AAAA-MM-DD

### Adicionado
- Novas funcionalidades

### Alterado
- Mudanças em funcionalidades existentes

### Corrigido
- Correções de bugs

### Removido
- Funcionalidades removidas

### Segurança
- Melhorias de segurança
```
