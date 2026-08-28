# CLAUDE.md — oficina-lambda
## FIAP Pós-Tech Software Architecture — Fase 3

---

## CONTEXTO

Este repositório implementa a **Function Serverless de autenticação por CPF** da Fase 3 do Tech Challenge.

**Account ID:** 302789973247
**Região:** sa-east-1

**Os 4 repositórios da Fase 3:**
- `oficina-lambda` ← este repositório
- `oficina-infra-db` — Terraform para RDS PostgreSQL
- `oficina-infra-k8s` — Terraform para cluster EKS
- `oficina-app` — Aplicação Spring Boot

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
│   └── handler.py              ← validar_cpf, buscar_cliente, gerar_token, lambda_handler
├── tests/
│   ├── __init__.py
│   └── test_handler.py         ← 6 testes unitários com pytest + mocks
├── .github/
│   └── workflows/
│       └── deploy.yml          ← CI: test → deploy-homolog → deploy-prod
├── template.yaml               ← SAM template (Runtime: python3.12, Timeout: 10s, Memory: 256MB)
├── requirements.txt            ← psycopg2-binary==2.9.9, PyJWT==2.8.0
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

---

## STATUS

- [x] `src/handler.py` — implementado
- [x] `tests/test_handler.py` — implementado
- [x] `template.yaml` — implementado
- [x] `requirements.txt` — implementado
- [x] `Makefile` — implementado
- [x] `.github/workflows/deploy.yml` — implementado
- [x] `README.md` — implementado
- [ ] Deploy na AWS — aguardando `oficina-infra-db` estar provisionado

---

## SECRETS NECESSÁRIOS NO GITHUB

| Secret | Valor |
|---|---|
| `AWS_ACCESS_KEY_ID` | credencial AWS |
| `AWS_SECRET_ACCESS_KEY` | credencial AWS |
| `DB_HOST` | endpoint do RDS (disponível após oficina-infra-db) |
| `DB_PORT` | 5432 |
| `DB_NAME` | oficina |
| `DB_USER` | oficina |
| `DB_PASSWORD` | senha do RDS |
| `JWT_SECRET` | mesmo secret da aplicação Spring Boot |

---

## COMO TESTAR LOCALMENTE

```bash
pip install -r requirements.txt pytest
python -m pytest tests/ -v
```

---

## PRÓXIMO PASSO

Provisionar o RDS em `oficina-infra-db` para obter o `DB_HOST` e configurar os secrets do GitHub.
