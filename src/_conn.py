import os
import pyodbc
from dotenv import load_dotenv
load_dotenv()

DRIVER = os.getenv("SQLSERVER_DRIVER", "ODBC Driver 18 for SQL Server")
HOST   = os.getenv("SQLSERVER_HOST", r"localhost\SQLEXPRESS")
DB     = os.getenv("SQLSERVER_DB", "RetailChurn")
TRUSTED= os.getenv("SQLSERVER_TRUSTED", "yes").lower() == "yes"
USER   = os.getenv("SQLSERVER_USERNAME", "")
PWD    = os.getenv("SQLSERVER_PASSWORD", "")
TR_CERT= os.getenv("SQLSERVER_TRUST_CERT", "yes")

def get_conn():
    if TRUSTED:
        conn_str = (
            f"DRIVER={{{DRIVER}}};SERVER={HOST};DATABASE={DB};"
            f"Trusted_Connection=yes;TrustServerCertificate={TR_CERT};"
        )
    else:
        conn_str = (
            f"DRIVER={{{DRIVER}}};SERVER={HOST};DATABASE={DB};"
            f"UID={USER};PWD={PWD};TrustServerCertificate={TR_CERT};"
        )
    return pyodbc.connect(conn_str)
