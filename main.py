
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
import json

app = FastAPI()

class AnaliseInput(BaseModel):
    cnpj: str
    razao_social: str
    tipo_empresa: str
    regime_tributario: str
    resultado: dict

db_config = {
    "dbname": "flowmindz_db",
    "user": "flowmindz_db_user",
    "password": "4S52rb1raqopNIwV3RSwfGGNUYY0tglS",
    "host": "dpg-d1r951umcj7s73allss0-a",
    "port": 5432
}

@app.post("/salvar_analise")
def salvar_analise(analise: AnaliseInput):
    try:
        conn = psycopg2.connect(**db_config)
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

        return { "status": "sucesso", "id": new_id }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao salvar: {str(e)}")
