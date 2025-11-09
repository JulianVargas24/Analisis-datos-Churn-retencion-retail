JG Analítica – Churn & Retención en Retail

Power BI (DirectQuery) + SQL Server Express + Python (pip/venv) + Automatización con Windows Task Scheduler

Objetivo: identificar clientes en alto riesgo de churn, monitorear ingresos y priorizar acciones de retención con un flujo reproducible y automatizado (ETL Python → SQL → Power BI).

[🎥 Demo: ]


1) Elevator pitch

Este proyecto convierte datos de ventas (Excel/CSV) en insights accionables para equipos de negocio:

Scoring de riesgo por cliente (ALTO / MEDIO / BAJO) y % Alto sobre el total.

Ingresos 12M/6M/3M y crecimiento MoM por riesgo y país.

Top 10 clientes en riesgo alto por contribución histórica.

Mapa de ingresos por país y evolución mensual.

Automatización diaria (o programable) con Python + SQL Server Express + Task Scheduler.

Visualización en Power BI con DirectQuery para refrescar al instante tras la ingesta.

2) Arquitectura
Excel/CSV (data/raw) 
   └── Python (venv, pandas) ──► Limpia/normaliza (src/01_extract_clean.py)
                                └► Carga en SQL Server (src/02_load_sqlserver.py)
                                     └► KPIs/Churn SQL (src/03_kpis_churn_sqlserver.py)
                                          └► Tablas DIM/FACT + snapshot

SQL Server Express (vistas/tablas normalizadas)
   └── Power BI (DirectQuery) ──► Dashboards: Resumen, Alertas ALTO, Tendencia

Automatización (Windows Task Scheduler)
   └── .bat orquesta venv + run_pipeline.py (logs con timestamp en /logs)


Fuente: Excel/CSV (/data/raw)
Modelo (star-like): dim_customer_metrics (riesgo, RFM, snapshots), fact_sales/v_sales_monthly, dimensiones de calendario/cliente/país.
Conexión: Power BI en DirectQuery (tablas clave).
Despliegue: PBIX local (opcional publicar a Service).

3) Dashboards (¿qué preguntas responden?)
3.1 Resumen (C-level / Comercial)

¿Cuántos clientes tenemos y cuántos están en ALTO riesgo?
KPIs: Clientes totales, Clientes ALTO, % ALTO.

¿Cuánto vendimos (12M) y dónde?
Ingresos 12M y Top país por ingresos riesgo 12M (mapa).

¿Quiénes son los 10 clientes más críticos en riesgo alto (histórico)?
Tabla con cliente, país, ingresos 12M, días sin comprar, frecuencia de órdenes.

¿Cuándo fue la última actualización y cuál es el estado del snapshot?
Días desde último snapshot y semáforo (actualizado/desactualizado).

3.2 Alertas ALTO (Equipo de Retención/CRM)

¿Cuánto dinero y órdenes representan los clientes ALTO?
KPIs: Total monetario, Total órdenes, Promedio días sin comprar.

¿Qué clientes ALTO debo contactar primero?
Tabla de facturas detallada (fecha, SKU, descripción, cantidad, precio, total).

¿Cómo evolucionan los ingresos de clientes ALTO en el último año?
Línea/columnas con Ingresos por mes.

3.3 Tendencia (Estrategia / BI)

¿Cómo cambian los ingresos 3M/6M/12M y el crecimiento % MoM?
KPIs y gráfico de Ingresos vs % MoM.

¿Cómo evoluciona por nivel de riesgo?
Línea por riesgo (ALTO/BAJO/MEDIO) en el tiempo.

¿Qué países concentran más ingresos y cómo cambian?
Barras por país (últimos 12 meses).

4) KPIs clave (ejemplos)

Clientes ALTO: COUNTROWS(FILTER(dim_customer_metrics, churn_risk="ALTO" && [snapshot_date]=max))

% ALTO: DIVIDE([Clientes ALTO], [Clientes totales])

Ingresos 12M: suma de ventas en los últimos 12 meses (medida con filtro temporal).

Crec. % MoM: (Ingresos_mes_actual - Ingresos_mes_anterior) / Ingresos_mes_anterior.

Las medidas DAX exactas pueden variar según tu esquema final; el repo incluye los scripts SQL y campos base.

5) Stack usado

Python: pandas, pyodbc/sqlalchemy; ejecución en venv (aislado).

SQL Server Express: staging, normalización, KPIs de churn y snapshots.

Power BI: DirectQuery para actualización inmediata; bookmarks, tooltips, selectors.

Automatización: Windows Task Scheduler + .bat (orquesta venv + pipeline).

Control & Logs: logs por ejecución con timestamp en /logs.

6) Estructura del repo
churn-retail/
├─ .venv/                     # entorno virtual (no subir a Git)
├─ data/
│  ├─ raw/                    # Excel/CSV de entrada
│  │  ├─ online_retail_II.xlsx
│  │  └─ processed/           # (opcional) backups post-proceso
│  └─ db/                     # scripts SQL/seed si aplica
├─ logs/                      # logs con timestamp: pipeline_YYYYMMDD_HHMM.log
├─ src/
│  ├─ _conn.py                # helper de conexión a SQL (usa .env)
│  ├─ 01_extract_clean.py     # limpieza/normalización
│  ├─ 02_load_sqlserver.py    # carga a SQL Server
│  ├─ 03_kpis_churn_sqlserver.py # crea métricas/tablas/vistas KPIs
│  └─ run_pipeline.py         # orquestador Python
├─ sql/
│  └─ kpis_churn.sql          # SQL de KPIs/churn (si lo separas)
├─ run_churn_pipeline.bat     # orquestador para Scheduler (activa venv + pipeline)
├─ Dashboard.pbix             # Power BI (DirectQuery)
└─ README.md

7) Configuración & ejecución local
7.1 Requisitos

Windows 10/11

Python 3.10+

SQL Server Express (instalado y corriendo)

Power BI Desktop

7.2 Variables de entorno (.env)

Crea .env en la raíz (no lo subas a Git):

SQLSERVER=localhost\SQLEXPRESS
SQLDB=churn_retail
SQLUSER=sa
SQLPWD=********


Si usas autenticación de Windows, ajusta el string de conexión en src/_conn.py.

7.3 Instalar dependencias
python -m venv .venv
.venv\Scripts\pip.exe install -r requirements.txt

7.4 Ejecutar pipeline (manual)
.venv\Scripts\python.exe .\src\run_pipeline.py


Revisa logs/pipeline_YYYYMMDD_HHMM.log → debe terminar con rc=0.

Valida en SQL:

SELECT MAX(snapshot_date) FROM dim_customer_metrics;

8) Automatización (Windows Task Scheduler)

Archivo .bat (en la raíz):

@echo off
setlocal enableextensions enabledelayedexpansion

cd /d "C:\Users\Julian\Desktop\churn-retail"
set "PY=.venv\Scripts\python.exe"

if not exist "logs" mkdir logs
set "STAMP=%date:~-4%%date:~3,2%%date:~0,2%_%time:~0,2%%time:~3,2%"
set LOG="logs\pipeline_%STAMP%.log"

echo ===== INICIO %date% %time% (.venv) ===== >> %LOG%
"%PY%" ".\src\run_pipeline.py" >> %LOG% 2>&1
set RC=%ERRORLEVEL%
echo ===== FIN %date% %time% (rc=%RC%) ===== >> %LOG%
exit /b %RC%


Programador de Tareas

Acción: cmd.exe

Argumentos:

/c "C:\Users\Julian\Desktop\churn-retail\run_churn_pipeline.bat"


Iniciar en:

C:\Users\Julian\Desktop\churn-retail


Condiciones: reintentos (3) cada 5 min, detener si excede X min (opcional).

“Ejecutar tanto si el usuario inició sesión como si no” (si corresponde).

Validación

Revisa el historial de la tarea y el último log en /logs/.

rc=0 en log ⇒ ok.

Abre PBIX (DirectQuery) y verifica KPIs/visuales actualizados.

9) Troubleshooting

ModuleNotFoundError: pandas
Asegúrate de que el .bat llama al python del venv (.venv\Scripts\python.exe) y que instalaste requirements.txt.

Errores de rutas/espacios
Usa rutas absolutas y comillas ("C:\…\run_pipeline.py").
Evita emojis o caracteres especiales en print() (pueden romper cp1252 en Windows).

Permisos SQL
El usuario debe tener permisos de CREATE/INSERT/UPDATE en la BD.
