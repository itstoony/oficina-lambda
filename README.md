# oficina-lambda

Function Serverless AWS Lambda para autenticação de clientes por CPF.

## Responsabilidade

1. Valida o CPF pelo algoritmo dos dois dígitos verificadores
2. Consulta o cliente no banco de dados RDS PostgreSQL
3. Gera e retorna um token JWT válido para consumo das APIs protegidas

## Tecnologias

| Tecnologia | Uso |
|---|---|
| Python 3.12 | Runtime da Lambda |
| AWS Lambda | Execução serverless |
| AWS API Gateway | Roteamento HTTP |
| AWS SAM CLI | Build e deploy |
| psycopg2 | Conexão com PostgreSQL |
| PyJWT | Geração de tokens JWT HS256 |

## Arquitetura

```
Cliente
  │
  ▼
AWS API Gateway
https://fpwmtfk2k4.execute-api.sa-east-1.amazonaws.com/Prod/auth/login
  │
  ▼
Lambda (oficina-autenticacao)
  ├── Valida CPF (algoritmo dígitos verificadores)
  ├── Consulta cliente no RDS PostgreSQL
  └── Retorna JWT HS256 (exp: 24h)
```

## Endpoint ativo

| Recurso | URL |
|---|---|
| **POST /auth/login** | `https://fpwmtfk2k4.execute-api.sa-east-1.amazonaws.com/Prod/auth/login` |
| **Postman Collection** | [postman/oficina-lambda.postman_collection.json](postman/oficina-lambda.postman_collection.json) |

```
Body:    { "cpf": "529.982.247-25" }
Sucesso: { "token": "eyJ...", "clienteId": "uuid", "nome": "Nome" }
Erro:    { "erro": "mensagem" }
```

## Fluxo de branches e CI/CD

```
develop → homolog (deploy automático) → main (deploy automático via PR)
```

- `main` protegida: PR obrigatório com 1 aprovação + CI verde
- Push em `homolog` → deploy automático em homologação
- Merge em `main` → deploy automático em produção
- Stack CloudFormation: `oficina-lambda-homolog` / `oficina-lambda-prod`

## Execução local

```bash
pip install -r requirements.txt pytest
python -m pytest tests/ -v
```

## Deploy manual

```bash
sam build && sam deploy --guided
```

## Secrets necessários no GitHub (por environment)

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
