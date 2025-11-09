# JG Analítica – Churn & Retención (Retail) · Power BI + SQL Server + Python

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](#)
[![SQL Server](https://img.shields.io/badge/SQL%20Server-2019+-CC2927?logo=microsoftsqlserver&logoColor=white)](#)
[![Power BI](https://img.shields.io/badge/Power%20BI-Desktop%20/Service-F2C811?logo=powerbi&logoColor=black)](#)
[![Automatizado](https://img.shields.io/badge/Pipeline-Automatizado-4CAF50?logo=windows-terminal&logoColor=white)](#)
[![Última actualización](https://img.shields.io/badge/Última%20actualización-hoy-blue)](#)

> Análisis operativo de **churn/retención** para retail con  
> **ingesta Python → SQL Server** y visualización en **Power BI**.  
> Pipeline **automatizado** vía *Windows Task Scheduler*.

**Demo**: *(próximamente)* • **Diseño**: Dark/metal con acentos **amarillo** para alertas.  

---

## Índice
1. [Elevator pitch](#1-elevator-pitch)  
2. [Arquitectura](#2-arquitectura)  
3. [Dashboards (qué preguntas responden)](#3-dashboards-qué-preguntas-responden)  
4. [KPIs clave](#4-kpis-clave)  
5. [Stack usado](#5-stack-usado-en-el-proyecto)  
6. [Impacto para el negocio](#6-impacto-para-el-negocio-contratemos-esto)  
7. [Cómo correr el proyecto](#7-cómo-correr-el-proyecto)  
8. [Automatización diaria](#8-automatización-diaria-opcional)  
9. [Estructura del repo](#9-estructura-del-repo)

---

## 1) Elevator pitch

Transformo ventas históricas en **decisiones accionables** para **reducir churn** y **aumentar retención**:

- Segmentación de **riesgo de churn** (**ALTO/MEDIO/BAJO**) y **% ALTO** en el tiempo.  
- **Top clientes en riesgo** (ingreso 12M, días sin comprar, frecuencia).  
- **Ingresos por país** y **crecimiento % MoM** para priorizar mercados.  
- **Python** + **SQL Server** para ingesta/curado; **Power BI** para exploración rápida.

> **Resultado esperado:** menor fuga, mayor recompra y foco comercial donde *sí* mueve la aguja.

---

## 2) Arquitectura

Python (pandas)
└──► SQL Server (tablas + vistas)
└──► Power BI (modelo / KPIs / visual)
▲
└── validaciones y carga (pipeline)

markdown
Copiar código

- **Fuente**: Excel `data/raw/online_retail_II.xlsx` (2010–2011).  
- **Ingesta**: scripts Python `01_extract_clean.py` (limpieza) y `02_load_sqlserver.py` (carga).  
- **KPIs/Churn**: SQL en `03_kpis_churn_sqlserver.py` (mediciones, snapshots, flags).  
- **Modelo**: star-like con hechos mensuales y dimensión clientes.  
- **Automatización**: `.bat` + **Programador de tareas** (diario 07:00).  
- **Despliegue**: PBIX local (opcional Power BI Service).

---

## 3) Dashboards (qué preguntas responden)

### 3.1 Resumen operativo
**Preguntas**  
- ¿Cuál es el **% de clientes en riesgo ALTO** hoy y cómo cambió vs. meses previos?  
- ¿Qué **clientes generan más ingreso** y están **dejando de comprar**?  
- ¿Dónde están los **ingresos de los últimos 12 meses** por país?

**Aporta a la empresa**  
- Priorización diaria de **contactos críticos** (alto ingreso + muchos días sin comprar).  
- **Enfoque comercial**: asignación de fuerza de ventas y campañas de retención.

> _Sugerencia_: coloca aquí un screenshot  
> `![Resumen](./images/resumen.png)`

---

### 3.2 Alertas ALTO (acción)
**Preguntas**  
- ¿Cuánto **dinero** y **órdenes** se concentran en el **segmento ALTO**?  
- ¿Cuándo fue la **última compra** de cada cliente y qué **patrón** de consumo tienen?  
- ¿Qué **SKU** o categorías empujan la recompra?

**Aporta a la empresa**  
- Lista **operable** para CRM/Outbound (WhatsApp, email, call center).  
- **Recomendaciones de producto** por historial para elevar conversión.

> _Sugerencia_: `![Alertas ALTO](./images/alertas_alto.png)`

---

### 3.3 Tendencia (crecimiento y riesgo)
**Preguntas**  
- ¿Cómo evolucionan **Ingresos 3M/6M/12M** y el **% ALTO**?  
- ¿Qué **países** explican el crecimiento y dónde cae la demanda?  
- ¿Cuál es el **% de crecimiento MoM** y su **estacionalidad**?

**Aporta a la empresa**  
- Planificación de **ventas y abastecimiento** por país.  
- **Reducción de volatilidad** anticipando caídas de recompra.

> _Sugerencia_: `![Tendencia](./images/tendencia.png)`

---

## 4) KPIs clave

- **% ALTO (Último)**: proporción de clientes en ALTO en el *último snapshot*.  
- **Ingresos móviles**: 3M / 6M / 12M.  
- **Clientes ALTO**: `DISTINCTCOUNT` en el último snapshot.  
- **Días desde último snapshot**: control de frescura de datos.

> Nota: se normalizan nulos (fechas/mes) para trazabilidad y consistencia de series.

---

## 5) Stack usado en el proyecto

- **Power BI** (DAX, drill-through, tooltips, bookmarks).  
- **SQL Server** (vistas, joins, normalización).  
- **Python** (pandas, pyodbc/sqlalchemy).  
- **Windows Task Scheduler** + `.bat` (automatización diaria).  
- **GitHub** (código, documentación, versionado).

---

## 6) Impacto para el negocio (contratemos esto)

- **–10–20% de fuga** en cohortes intervenidas (benchmarks típicos de programas de retención).  
- **+5–12% de ingresos** por recompra en 60–90 días focalizando clientes ALTO.  
- **Ahorro de tiempo**: pipeline diario, sin “copiar/pegar” ni procesos manuales.  
- **Escalable**: agregar nuevas fuentes (ERP, e-commerce, CRM) sin cambiar el front.

> **Rol aportado**: Data/BI Analyst que diseña el modelo de datos, arma KPIs accionables y deja la operación **automatizada** para equipo comercial & dirección.

---

## 7) Cómo correr el proyecto

- 1) Clonar el repo
git clone https://github.com/<tu-usuario>/<tu-repo>.git
cd <tu-repo>

- 2) Crear y activar venv (Windows)
python -m venv .venv
.\.venv\Scripts\activate

- 3) Instalar requerimientos
pip install -r requirements.txt

- 4) Crear .env (credenciales/DSN)
copy .env.example .env
edita con tus datos de SQL Server / DSN

- 5) Poner el Excel en data/raw/ (online_retail_II.xlsx)
     
- 6) Ejecutar el pipeline orquestador
python .\src\run_pipeline.py
El orquestador ejecuta:
01_extract_clean.py → 02_load_sqlserver.py → 03_kpis_churn_sqlserver.py
y guarda logs en logs/.

---

## 8) Automatización diaria (opcional)
Se incluye run_churn_pipeline.bat para ejecutar el pipeline con el venv correcto.

Programar en Programador de tareas a las 07:00 (trigger diario).

La salida queda registrada en logs/pipeline_YYYY-MM-DD_HHMM.log.

<img width="1457" height="818" alt="Image" src="https://github.com/user-attachments/assets/d548e93f-6397-4184-9944-df5397edfc86" />
<img width="1454" height="817" alt="image" src="https://github.com/user-attachments/assets/9b3cc853-655b-498a-b350-318a0dd8ddd3" />
<img width="1451" height="812" alt="Image" src="https://github.com/user-attachments/assets/e1725e30-61be-4fc5-b49a-1c83c7e4a372" />
<img width="1560" height="983" alt="Image" src="https://github.com/user-attachments/assets/c2566e77-8e3e-4305-9de0-ab103144f406" />
<img width="1920" height="1021" alt="Image" src="https://github.com/user-attachments/assets/f86a77b1-ef15-4f72-b782-88652b951c3e" />
<img width="628" height="478" alt="Image" src="https://github.com/user-attachments/assets/b2578774-9bfa-4a00-962f-78eb82414820" />







