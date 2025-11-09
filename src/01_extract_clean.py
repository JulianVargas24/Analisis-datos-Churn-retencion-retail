# src/01_extract_clean.py
from pathlib import Path
import pandas as pd
import re

RAW = Path("data/raw")
PROC = Path("data/processed")
PROC.mkdir(parents=True, exist_ok=True)

def normalize_cols(cols):
    out = []
    for c in cols:
        c = c.strip()
        c = re.sub(r"\s+", "_", c)       # espacios -> _
        c = c.replace("/", "_")
        c = c.replace("-", "_")
        c = c.replace(".", "")
        c = c.lower()
        out.append(c)
    return out

def pick(df_cols, *aliases):
    """Devuelve el primer alias que exista en df_cols."""
    for a in aliases:
        if a in df_cols:
            return a
    raise KeyError(f"No se encontró ninguna de las columnas: {aliases}")

# 1) Leer Excel (o CSVs si hubiera)
excel_files = list(RAW.glob("*.xlsx")) + list(RAW.glob("*.xls"))
csv_files   = list(RAW.glob("*.csv"))
dfs = []

if excel_files:
    xfile = excel_files[0]
    print(f"Leyendo Excel: {xfile.name}")
    xl = pd.ExcelFile(xfile)
    sheets = xl.sheet_names
    candidatos = ["Year 2009-2010", "2009-2010", "Year 2010-2011", "2010-2011"]
    target = [s for s in candidatos if s in sheets] or sheets
    for s in target:
        print(f" - Hoja: {s}")
        dfs.append(pd.read_excel(xfile, sheet_name=s))
elif csv_files:
    print("Leyendo CSVs:")
    for f in csv_files:
        print(" -", f.name)
        dfs.append(pd.read_csv(f, encoding="ISO-8859-1"))
else:
    raise SystemExit("Pon tu Excel/CSV en data/raw/")

df = pd.concat(dfs, ignore_index=True)

# 2) Normalizar nombres de columnas y mostrar para debug
orig_cols = list(df.columns)
df.columns = normalize_cols(df.columns)
print("Columnas detectadas (normalizadas):", list(df.columns))

# 3) Elegir columnas usando sinónimos
col_invoice     = pick(df.columns, "invoiceno", "invoice", "invoice_no")
col_stockcode   = pick(df.columns, "stockcode", "stock_code")
col_desc        = pick(df.columns, "description", "desc")
col_quantity    = pick(df.columns, "quantity", "qty")
col_invoicedate = pick(df.columns, "invoicedate", "invoice_date", "date")
col_price       = pick(df.columns, "unitprice", "price", "unit_price")
col_customerid  = pick(df.columns, "customerid", "customer_id", "customerid_")
col_country     = pick(df.columns, "country")

# 4) Subset + renombrar al esquema final
df = df[[
    col_invoice, col_stockcode, col_desc, col_quantity,
    col_invoicedate, col_price, col_customerid, col_country
]].rename(columns={
    col_invoice: "invoice_no",
    col_stockcode: "stock_code",
    col_desc: "description",
    col_quantity: "quantity",
    col_invoicedate: "invoice_date",
    col_price: "unit_price",
    col_customerid: "customer_id",
    col_country: "country"
})

# 5) Limpieza
df = df.dropna(subset=["customer_id"])
# Algunas hojas traen IDs como float; conviértelo a int si aplica
df["customer_id"] = pd.to_numeric(df["customer_id"], errors="coerce")
df = df.dropna(subset=["customer_id"])
df["customer_id"] = df["customer_id"].astype(int)

df = df[pd.to_numeric(df["quantity"], errors="coerce").notna()]
df["quantity"] = df["quantity"].astype(int)
df = df[pd.to_numeric(df["unit_price"], errors="coerce").notna()]
df["unit_price"] = df["unit_price"].astype(float)

df["invoice_date"] = pd.to_datetime(df["invoice_date"], errors="coerce")
df = df.dropna(subset=["invoice_date"])
df = df[(df["quantity"] > 0) & (df["unit_price"] > 0)]

# 6) Fecha ISO y guardar
df["invoice_date"] = df["invoice_date"].dt.strftime("%Y-%m-%d")

OUT = PROC / "retail_clean.csv"
df.to_csv(OUT, index=False, encoding="utf-8")
print(f"Limpieza lista: {OUT}")
