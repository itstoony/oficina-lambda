# oficina-lambda

Function Serverless AWS Lambda para autenticação de clientes por CPF.

## Responsabilidade

1. Valida o CPF pelo algoritmo dos dois dígitos verificadores
2. Consulta o cliente no banco de dados RDS PostgreSQL
3. Gera e retorna um token JWT válido para consumo das APIs protegidas

## Tecnologias

- Python 3.12
- AWS Lambda + API Gateway
- AWS SAM CLI
- psycopg2 (PostgreSQL)
- PyJWT

## Endpoint

```
POST /auth/login
Body: { "cpf": "529.982.247-25" }
Response: { "token": "eyJ...", "clienteId": "uuid", "nome": "Nome" }
```

## Execução local

```bash
pip install -r requirements.txt
sam build
sam local start-api
curl -X POST http://localhost:3000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"cpf": "529.982.247-25"}'
```

## Testes

```bash
pip install pytest
python -m pytest tests/ -v
```

## Deploy manual

```bash
sam build && sam deploy --guided
```

## CI/CD

- Push em `homolog` → deploy automático em homologação
- Push em `main` (via PR) → deploy automático em produção

## Secrets necessários no GitHub

| Secret | Descrição |
|---|---|
| `AWS_ACCESS_KEY_ID` | Credencial AWS |
| `AWS_SECRET_ACCESS_KEY` | Credencial AWS |
| `DB_HOST` | Endpoint do RDS (disponível após oficina-infra-db) |
| `DB_PORT` | Porta do banco (5432) |
| `DB_NAME` | Nome do banco (oficina) |
| `DB_USER` | Usuário do banco (oficina) |
| `DB_PASSWORD` | Senha do RDS |
| `JWT_SECRET` | Mesmo secret usado na aplicação Spring Boot |
