# Deploy

Este guia aborda a implantação da API em ambiente de produção.

## Preparação para Produção

### 1. Configurações de Produção

#### Variáveis de Ambiente

Crie um `.env` específico para produção:

```env
# Banco de Dados (PostgreSQL recomendado)
DATABASE_URL=postgresql+asyncpg://usuario:senha@localhost:5432/car_api_db

# JWT
JWT_SECRET_KEY=<chave_secreta_forte_gerada>
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=30
```

> **Importante**: Nunca commite o arquivo `.env` no repositório.

#### Banco de Dados

Em produção, utilize um banco de dados robusto:

| Banco | Driver SQLAlchemy | Recomendação |
|-------|-------------------|--------------|
| PostgreSQL | `asyncpg` | ✅ Recomendado |
| MySQL | `aiomysql` | ✅ Bom |
| SQLite | `aiosqlite` | ❌ Apenas dev/testes |

**Instalar driver PostgreSQL:**

```bash
poetry add asyncpg
```

### 2. Aplicar Migrações

Antes de iniciar a aplicação, aplique as migrações:

```bash
poetry run alembic upgrade head
```

### 3. Servidor ASGI

Para produção, utilize um servidor ASGI como **Uvicorn** ou **Gunicorn**.

**Instalar:**

```bash
poetry add uvicorn gunicorn
```

**Executar com Uvicorn:**

```bash
poetry run uvicorn car_api.app:app \
    --host 0.0.0.0 \
    --port 8000 \
    --workers 4 \
    --log-level info
```

**Executar com Gunicorn + Uvicorn Workers:**

```bash
poetry run gunicorn car_api.app:app \
    -w 4 \
    -k uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000
```

## Docker

### Dockerfile

Crie um `Dockerfile` na raiz do projeto:

```dockerfile
FROM python:3.13-slim

WORKDIR /app

# Instalar Poetry
RUN pip install poetry==2.0.0

# Copiar arquivos de dependência
COPY pyproject.toml poetry.lock ./

# Instalar dependências
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --only main

# Copiar código fonte
COPY . .

# Expor porta
EXPOSE 8000

# Comando de execução
CMD ["uvicorn", "car_api.app:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

### docker-compose.yml

Crie `docker-compose.yml`:

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql+asyncpg://carapi:secret@db:5432/carapi
      - JWT_SECRET_KEY=${JWT_SECRET_KEY}
      - JWT_ALGORITHM=HS256
      - JWT_EXPIRATION_MINUTES=30
    depends_on:
      - db
    networks:
      - carapi_network

  db:
    image: postgres:16-alpine
    environment:
      - POSTGRES_USER=carapi
      - POSTGRES_PASSWORD=secret
      - POSTGRES_DB=carapi
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - carapi_network

  migrations:
    build: .
    command: alembic upgrade head
    environment:
      - DATABASE_URL=postgresql+asyncpg://carapi:secret@db:5432/carapi
    depends_on:
      - db
    networks:
      - carapi_network

networks:
  carapi_network:
    driver: bridge

volumes:
  postgres_data:
```

**Executar:**

```bash
docker-compose up -d
```

## Cloud Providers

### Railway

1. Conecte seu repositório GitHub
2. Configure variáveis de ambiente no dashboard
3. Railway detecta automaticamente o `pyproject.toml`
4. Deploy automático a cada push

**Variáveis necessárias:**
- `DATABASE_URL`
- `JWT_SECRET_KEY`

### Render

1. Crie um Web Service
2. Configure o build command:
   ```bash
   pip install poetry==2.0.0 && poetry install --only main --no-interaction
   ```
3. Start command:
   ```bash
   uvicorn car_api.app:app --host 0.0.0.0 --port $PORT --workers 4
   ```

### AWS (ECS/EKS)

Para AWS, utilize containers Docker:

1. Build e push da image para ECR
2. Configure ECS task definition
3. Deploy via ECS ou EKS
4. Utilize RDS para banco de dados PostgreSQL
5. Configure Secrets Manager para `JWT_SECRET_KEY`

### Heroku

Crie `Procfile`:

```
web: uvicorn car_api.app:app --host 0.0.0.0 --port $PORT --workers 4
```

**Deploy:**

```bash
heroku create
heroku config:set JWT_SECRET_KEY=$(python -c "import secrets; print(secrets.token_urlsafe(32))")
heroku addons:create heroku-postgresql:mini
git push heroku main
heroku run alembic upgrade head
```

## Nginx (Reverse Proxy)

Configure Nginx como reverse proxy:

```nginx
server {
    listen 80;
    server_name api.seudominio.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## SSL/TLS

Utilize Let's Encrypt para HTTPS gratuito:

```bash
sudo certbot --nginx -d api.seudominio.com
```

## Health Check

Configure health checks para monitoramento:

```
GET /health_check
Response: {"status": "ok"}
```

**Exemplo Kubernetes:**

```yaml
livenessProbe:
  httpGet:
    path: /health_check
    port: 8000
  initialDelaySeconds: 10
  periodSeconds: 30
```

## Monitoramento

### Logs

Configure logging estruturado:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### APM (Application Performance Monitoring)

Considere ferramentas como:
- **Sentry** - Rastreamento de erros
- **New Relic** - Monitoramento de performance
- **Datadog** - Observabilidade completa

## Checklist de Deploy

- [ ] Variáveis de ambiente configuradas
- [ ] `JWT_SECRET_KEY` forte e único gerado
- [ ] Banco de dados configurado (PostgreSQL recomendado)
- [ ] Migrações aplicadas (`alembic upgrade head`)
- [ ] Servidor ASGI configurado (Uvicorn/Gunicorn)
- [ ] HTTPS habilitado
- [ ] Health check configurado
- [ ] Logs centralizados
- [ ] Backup do banco automatizado
- [ ] Firewall configurado (apenas portas necessárias)
- [ ] CORS configurado para origens permitidas
- [ ] Testes executados e passando

## Rollback

Em caso de problemas:

1. **Reverter migração:**
   ```bash
   alembic downgrade -1
   ```

2. **Deploy versão anterior:**
   ```bash
   git checkout <commit_anterior>
   git push origin main --force
   ```

3. **Restaurar backup do banco** (se necessário)
