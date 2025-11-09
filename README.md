JG Analítica – Churn & Retención (Retail) · Power BI + SQL Server + Python

Análisis operativo de churn/retención para retail con ingesta Python → SQL Server y visualización en Power BI.
Incluye automatización diaria con Windows Task Scheduler + .bat + venv.

🎬 Demo (próximamente)
 · 📊 PBIX (opcional)

1) Elevator pitch

Este proyecto convierte datos transaccionales (ventas y clientes) en decisiones accionables para retención:

¿Cuántos clientes están en riesgo (ALTO/MEDIO/BAJO) y cómo evoluciona el % ALTO?

¿Qué países/segmentos concentran mayor ingreso de clientes en riesgo?

¿Qué clientes específicos debería contactar hoy (ALTO riesgo) y con qué historial de compra?

¿Estamos creciendo mes a mes? ¿Qué tan volátil es el % de churn?

Automatizado: Python limpia/ingesta el Excel a SQL Server y refrezca el modelo; Power BI queda listo para consultar.

2) Arquitectura

Python (pandas) → SQL Server (tablas + vistas) → Power BI (modelo semántico)
↳ Orquestación con .bat + Task Scheduler (activa venv y ejecuta pipeline).

Fuente: Excel local (/data/raw/online_retail_II.xlsx → hojas 2010–2011).

Ingesta: 01_extract_clean.py (limpieza), 02_load_sqlserver.py (carga), 03_kpis_churn_sqlserver.py (KPIs/churn).

Modelo: star-like con dimensión de clientes y hechos (ventas mensuales).

Conexión: Power BI con tablas modeladas (puedes usar Import o DirectQuery si mueves a un SQL remoto).

Automatización: .bat + Programador de tareas (diario 07:00).

3) Dashboards (¿qué preguntas responden?)
3.1 Resumen (visión ejecutiva)

Total clientes y % ALTO (último snapshot).

Ingresos 12M y Top país ingreso riesgo 12M.

Riesgos de clientes (ALTO/MEDIO/BAJO).

Top 10 clientes en riesgo alto + detalle de órdenes recientes.

Mapa: ingresos últimos 12 meses por país.

Insight: prioriza ALTO con alto ingreso y muchos días sin comprar.

3.2 Alertas ALTO (acción operativa)

Total monetario + Total órdenes del segmento ALTO.

Promedio de días sin comprar y última compra (tabla).

Serie de ingresos del grupo ALTO (mes a mes).

Tabla de detalle (facturas, SKU, cantidad, precio unitario).

Insight: identifica clientes/itinerarios para campañas de retención inmediatas.

3.3 Tendencia (visión temporal)

Ingresos 3M / 6M / 12M (KPIs rápidos).

Ingresos por país (ranking) y crecimiento % MoM.

Ingresos por riesgo (líneas ALTO/MEDIO/BAJO).

Insight: detecta meses estacionales y evalúa el impacto de iniciativas de retención.

4) KPIs clave (DAX / SQL)

Nota: los nombres pueden variar levemente según tus tablas/medidas.

% ALTO (Último)

'% ALTO (Último)' =
VAR _snap =
  CALCULATE( MAX(dim_customer_metrics[snapshot_date]), ALL(dim_customer_metrics[snapshot_date]) )
VAR _num =
  CALCULATE(
    DISTINCTCOUNT(dim_customer_metrics[customer_id]),
    dim_customer_metrics[snapshot_date] = _snap,
    KEEPFILTERS( VALUES(dim_customer_metrics[churn_risk]) ),
    dim_customer_metrics[churn_risk] = "ALTO"
  )
VAR _den =
  CALCULATE(
    DISTINCTCOUNT(dim_customer_metrics[customer_id]),
    dim_customer_metrics[snapshot_date] = _snap
  )
RETURN DIVIDE(_num,_den,0)


Ingresos 12M / 6M / 3M (medidas de periodo móvil con v_sales_monthly).

Clientes ALTO (distintos en último snapshot).

Días desde último snapshot (control de frescura de datos).

5) Stack usado

Power BI: KPI cards, slices, mapas, líneas/columnas; bookmarks/botones de menú.

SQL Server: vistas/tablas normalizadas para consumo; cálculos server-side de churn y métricas.

Python (pandas, pyodbc o sqlalchemy): limpieza, ingesta, KPIs.

Automatización: Windows Task Scheduler + .bat (activa venv y lanza pipeline).

Control de versiones: Git/GitHub (+ .gitignore para .env, logs, datos crudos).

6) Automatización diaria

Programador de tareas (Windows) ejecuta run_churn_pipeline.bat a las 07:00:

@echo off
setlocal enabledelayedexpansion

REM 1) Ir a la carpeta del proyecto
cd /d "C:\Users\Julian\Desktop\churn-retail"

REM 2) Python del venv (ajusta si tu venv se llama distinto)
set "PY=.\.venv\Scripts\python.exe"

REM 3) Asegurar carpeta de logs
if not exist "logs" mkdir logs
set "XLOGDIR=logs"
set "STAMP=%date:~6,4%-%date:~3,2%-%date:~0,2%_%time:~0,2%h%time:~3,2%m"
set "XLOG=%XLOGDIR%\pipeline_%STAMP%.log"

REM 4) Ejecutar orquestador Python (capturar salida en Log)
echo ===== INICIO %date% %time% (venv) ===== >> "%XLOG%"
"%PY%" ".\src\run_pipeline.py" >> "%XLOG%" 2>&1
set "RC=%ERRORLEVEL%"
echo ===== FIN %date% %time% (rc=%RC%) ===== >> "%XLOG%"

exit /b %RC%


Importante: el .bat activa el Python del venv y levanta los 3 scripts (01_extract_clean.py, 02_load_sqlserver.py, 03_kpis_churn_sqlserver.py) desde run_pipeline.py.

7) Cómo correr local (setup rápido)
# 1) Clonar
git clone https://github.com/<tu-usuario>/Analisis-datos-Churn-retencion-retail.git
cd Analisis-datos-Churn-retencion-retail

# 2) Crear venv e instalar
python -m venv .venv
.\.venv\Scripts\pip install --upgrade pip
.\.venv\Scripts\pip install -r requirements.txt

# 3) Variables de entorno
copy .env.example .env
# → edita .env con tus credenciales de SQL Server

# 4) Dejar Excel en data/raw
#    (online_retail_II.xlsx con hojas 2010–2011)

# 5) Probar pipeline
.\.venv\Scripts\python.exe .\src\run_pipeline.py


.env.example (incluido en el repo)

SQL_SERVER=localhost\SQLEXPRESS
SQL_DB=churn_retail
SQL_USER=sa
SQL_PASSWORD=tu_password
SQL_TRUSTED=Yes      # si usas auth integrada, ajusta en tu código

8) Estructura del repo
churn-retail/
├─ .venv/                 # entorno (ignorado)
├─ data/
│  ├─ raw/                # NO versionar Excel/CSV locales
│  │  └─ README.md
│  └─ processed/          # temporales (opcional)
├─ db/                    # scripts SQL (opcional)
├─ logs/                  # .log de pipeline (ignorado)
├─ src/
│  ├─ 01_extract_clean.py
│  ├─ 02_load_sqlserver.py
│  ├─ 03_kpis_churn_sqlserver.py
│  ├─ run_pipeline.py
│  └─ _conn.py            # helper de conexión
├─ run_churn_pipeline.bat
├─ Dashboard.pbix
├─ Diseño resumen.png     # imágenes para README
├─ Diseño alto.png
├─ Diseño tendencia.png
├─ requirements.txt
├─ .env.example
├─ .gitignore
└─ README.md
