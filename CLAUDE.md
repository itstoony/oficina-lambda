# CLAUDE.md — oficina-lambda
## FIAP Pós-Tech Software Architecture — Fase 3

---

## CONTEXTO

Este repositório implementa a **Function Serverless de autenticação por CPF** da Fase 3 do Tech Challenge.

**Account ID:** 302789973247
**Região:** sa-east-1

**Os 4 repositórios da Fase 3:**
- `oficina-lambda` ← este repositório — **CONCLUÍDO**
- `oficina-infra-db` — Terraform para RDS PostgreSQL
- `oficina-infra-k8s` — Terraform para cluster EKS
- `oficina-app` (fiap-oficina) — Aplicação Spring Boot

---

## RESPONSABILIDADE

A Lambda recebe um CPF via POST, valida pelo algoritmo dos dois dígitos verificadores, consulta o cliente no RDS e retorna um JWT assinado com HS256.

Endpoint: `POST /auth/login` → `{ "cpf": "529.982.247-25" }`

---

## ESTRUTURA

```
oficina-lambda/
├── src/
│   ├── __init__.py
│   ├── handler.py              ← validar_cpf, buscar_cliente, gerar_token, lambda_handler
│   └── requirements.txt        ← dependências empacotadas pelo SAM
├── tests/
│   ├── __init__.py
│   └── test_handler.py         ← 6 testes unitários com pytest + mocks
├── postman/
│   └── oficina-lambda.postman_collection.json
├── .github/
│   └── workflows/
│       ├── ci.yml              ← testes automáticos em push/PR
│       └── deploy.yml          ← deploy automático por branch
├── template.yaml               ← SAM template (Runtime: python3.12, Timeout: 10s, Memory: 256MB)
├── requirements.txt            ← dependências para desenvolvimento local e CI
├── Makefile                    ← install | test | build | local | deploy | deploy-ci
└── README.md
```

---

## DECISÕES TÉCNICAS

- **Runtime:** Python 3.12
- **JWT:** HS256, expiração em 24h, mesmo secret da aplicação Spring Boot
- **Banco:** consulta direto no RDS via psycopg2 (sem ORM)
- **Variáveis de ambiente:** todas via SAM Parameters → sem hardcode de credenciais
- **CORS:** `Access-Control-Allow-Origin: *` no header de resposta
- **Encoding:** `ensure_ascii=False` no json.dumps para retornar acentos corretamente

---

## BRANCHES E CI/CD

| Branch | Propósito | Deploy |
|---|---|---|
| `develop` | desenvolvimento | só CI (testes) |
| `homolog` | homologação | deploy automático ao receber push |
| `main` | produção | deploy automático ao receber merge de PR |

- `main` protegida: sem commits diretos, PR obrigatório com 1 aprovação, CI deve passar
- Bucket S3 para artefatos SAM: `oficina-sam-artifacts-302789973247`

---

## INFRAESTRUTURA PROVISIONADA

- **Lambda:** `oficina-autenticacao` (sa-east-1)
- **API Gateway:** `https://fpwmtfk2k4.execute-api.sa-east-1.amazonaws.com/Prod/auth/login`
- **Stack CloudFormation homolog:** `oficina-lambda-homolog`
- **Stack CloudFormation prod:** `oficina-lambda-prod` (aguardando merge para main)

---

## STATUS

- [x] `src/handler.py` — implementado e deployado
- [x] `tests/test_handler.py` — implementado
- [x] `template.yaml` — implementado
- [x] `requirements.txt` + `src/requirements.txt` — implementado
- [x] `Makefile` — implementado
- [x] `.github/workflows/ci.yml` — implementado
- [x] `.github/workflows/deploy.yml` — implementado
- [x] `postman/` — collection de testes criada
- [x] Deploy em homolog — funcionando na AWS
- [ ] Deploy em produção — aguarda RDS (`DB_HOST` real)

---

## SECRETS NO GITHUB (environment: homolog e production)

| Secret | Valor |
|---|---|
| `AWS_ACCESS_KEY_ID` | cadastrado |
| `AWS_SECRET_ACCESS_KEY` | cadastrado |
| `DB_HOST` | `placeholder` — atualizar após provisionar RDS |
| `DB_PORT` | `5432` |
| `DB_NAME` | `oficina` |
| `DB_USER` | `oficina` |
| `DB_PASSWORD` | cadastrado |
| `JWT_SECRET` | cadastrado |

---

## PRÓXIMO PASSO

Provisionar o RDS em `oficina-infra-db`, obter o endpoint e atualizar o secret `DB_HOST`.
