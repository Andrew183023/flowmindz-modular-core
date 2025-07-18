from utils.db_utils import get_connection

def init_database():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS analises_tributarias (
        id SERIAL PRIMARY KEY,
        cnpj TEXT,
        razao_social TEXT,
        tipo_empresa TEXT,
        regime_tributario TEXT,
        resultado JSONB,
        criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("🟢 Banco de dados inicializado com sucesso.")
