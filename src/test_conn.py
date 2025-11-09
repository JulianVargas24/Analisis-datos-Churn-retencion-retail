from _conn import get_conn
with get_conn() as conn:
    cur = conn.cursor()
    cur.execute("SELECT GETUTCDATE();")
    print("OK SQL Server:", cur.fetchone()[0])
