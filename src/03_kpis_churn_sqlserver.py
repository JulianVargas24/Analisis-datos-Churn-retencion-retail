from _conn import get_conn

with get_conn() as conn:
    cur = conn.cursor()
    with open("sql/kpis_churn.sql", "r", encoding="utf-8") as f:
        sql = f.read()
    cur.execute(sql)
    conn.commit()

print("KPIs y riesgo de churn calculados (dim_customer_metrics actualizada)")
