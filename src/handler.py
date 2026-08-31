import json
import os
import re
import boto3
import psycopg2
import jwt
from datetime import datetime, timedelta, timezone

# Configurações via variáveis de ambiente
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_NAME = os.environ.get("DB_NAME", "oficina")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
JWT_SECRET = os.environ.get("JWT_SECRET")
JWT_EXPIRATION_HOURS = int(os.environ.get("JWT_EXPIRATION_HOURS", "24"))


def validar_cpf(cpf: str) -> bool:
    """Valida CPF pelo algoritmo dos dois dígitos verificadores."""
    cpf = re.sub(r"[^0-9]", "", cpf)
    if len(cpf) != 11:
        return False
    if len(set(cpf)) == 1:
        return False
    # Primeiro dígito verificador
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    primeiro = 11 - (soma % 11)
    if primeiro >= 10:
        primeiro = 0
    if primeiro != int(cpf[9]):
        return False
    # Segundo dígito verificador
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    segundo = 11 - (soma % 11)
    if segundo >= 10:
        segundo = 0
    if segundo != int(cpf[10]):
        return False
    return True


def buscar_cliente(cpf: str) -> dict | None:
    """Busca cliente no RDS pelo CPF."""
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        connect_timeout=5
    )
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, nome, email FROM clientes WHERE documento_numero = %s",
                (cpf,)
            )
            row = cur.fetchone()
            if row:
                return {"id": str(row[0]), "nome": row[1], "email": row[2]}
            return None
    finally:
        conn.close()


def gerar_token(cliente: dict, cpf: str) -> str:
    """Gera JWT com os dados do cliente."""
    payload = {
        "sub": cpf,
        "clienteId": cliente["id"],
        "nome": cliente["nome"],
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + timedelta(hours=JWT_EXPIRATION_HOURS),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")


def resposta(status: int, body: dict) -> dict:
    return {
        "statusCode": status,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps(body, ensure_ascii=False),
    }


def lambda_handler(event, context):
    """Entry point da Lambda."""
    try:
        body = json.loads(event.get("body") or "{}")
        cpf_raw = body.get("cpf", "").strip()

        if not cpf_raw:
            return resposta(400, {"erro": "CPF é obrigatório"})

        cpf = re.sub(r"[^0-9]", "", cpf_raw)

        if not validar_cpf(cpf):
            return resposta(400, {"erro": "CPF inválido"})

        cliente = buscar_cliente(cpf)
        if not cliente:
            return resposta(404, {"erro": "Cliente não encontrado"})

        token = gerar_token(cliente, cpf)

        return resposta(200, {
            "token": token,
            "clienteId": cliente["id"],
            "nome": cliente["nome"],
        })

    except psycopg2.Error as e:
        print(f"[ERROR] Banco de dados: {e}")
        return resposta(503, {"erro": "Serviço temporariamente indisponível"})
    except Exception as e:
        print(f"[ERROR] Inesperado: {e}")
        return resposta(500, {"erro": "Erro interno"})
