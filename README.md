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

