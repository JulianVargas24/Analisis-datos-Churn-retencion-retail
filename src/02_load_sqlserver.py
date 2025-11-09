import pandas as pd
from pathlib import Path
from _conn import get_conn

clean_path = Path("data/processed/retail_clean.csv")
if not clean_path.exists():
    raise SystemExit("Primero corre 01_extract_clean.py")

df = pd.read_csv(clean_path)

with get_conn() as conn:
    cur = conn.cursor()
    # Si quieres recarga completa cada vez:
    cur.execute("TRUNCATE TABLE dbo.fact_sales;")
    conn.commit()

    insert_sql = """
    INSERT INTO dbo.fact_sales
    (invoice_no, stock_code, description, quantity, invoice_date, unit_price, customer_id, country)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """
    cur.fast_executemany = True

    # Inserción por lotes (evita saturar memoria)
    batch_size = 50000
    for i in range(0, len(df), batch_size):
        rows = df.iloc[i:i+batch_size].values.tolist()
        cur.executemany(insert_sql, rows)
        conn.commit()
        print(f" --> Insertadas {i+len(rows):,} filas")

print("Carga completada en dbo.fact_sales")
