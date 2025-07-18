from fastapi import FastAPI
from dotenv import load_dotenv
import os
import psycopg2
import json
from pydantic import BaseModel
from utils.db_utils import get_connection


load_dotenv()  # Carrega variáveis do .env

app = FastAPI()

class AnaliseInput(BaseModel):
    cnpj: str
    razao_social: str
    tipo_empresa: str
    regime_tributario: str
    resultado: dict

# Pega as variáveis do .env
db_config = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
}

@app.post("/salvar_analise")
def salvar_analise(analise: AnaliseInput):
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO analises_tributarias (cnpj, razao_social, tipo_empresa, regime_tributario, resultado)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id;
        """, (
            analise.cnpj,
            analise.razao_social,
            analise.tipo_empresa,
            analise.regime_tributario,
            json.dumps(analise.resultado)
        ))

        new_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()

        return {"status": "sucesso", "id": new_id}
    except Exception as e:
        return {"status": "erro", "detalhe": str(e)}

