/* KPIs por cliente */
IF OBJECT_ID('tempdb..#kpi') IS NOT NULL DROP TABLE #kpi;
SELECT
  fs.customer_id,
  MAX(fs.invoice_date)           AS last_purchase_date,
  COUNT(DISTINCT fs.invoice_no)  AS frequency_orders,
  SUM(CAST(fs.quantity * fs.unit_price AS DECIMAL(18,2))) AS monetary_value
INTO #kpi
FROM dbo.fact_sales fs
GROUP BY fs.customer_id;

/* Recency */
/* Usar el fin del dataset como "hoy" para que la recencia sea realista */
DECLARE @today DATE = DATEADD(DAY, 1, (SELECT MAX(invoice_date) FROM dbo.fact_sales));
IF OBJECT_ID('tempdb..#kpi2') IS NOT NULL DROP TABLE #kpi2;
SELECT
  customer_id,
  last_purchase_date,
  DATEDIFF(DAY, last_purchase_date, @today) AS recency_days,
  frequency_orders,
  monetary_value
INTO #kpi2
FROM #kpi;

/* P25 monetario (aprox por cuartiles) */
DECLARE @p25 DECIMAL(18,2);
;WITH q AS (
  SELECT monetary_value,
         NTILE(4) OVER (ORDER BY monetary_value ASC) AS nt
  FROM #kpi2
)
SELECT @p25 = MIN(monetary_value) FROM q WHERE nt = 1;

/* Etiqueta de riesgo */
IF OBJECT_ID('tempdb..#kpi3') IS NOT NULL DROP TABLE #kpi3;
SELECT
  customer_id,
  last_purchase_date,
  recency_days,
  frequency_orders,
  monetary_value,
  CASE
    WHEN recency_days >= 90 OR (frequency_orders <= 2 AND monetary_value <= @p25) THEN 'ALTO'
    WHEN recency_days >= 60 THEN 'MEDIO'
    ELSE 'BAJO'
  END AS churn_risk,
  @today AS snapshot_date
INTO #kpi3
FROM #kpi2;

/* Upsert a la dimensión */
MERGE dbo.dim_customer_metrics AS T
USING #kpi3 AS S
ON (T.customer_id = S.customer_id)
WHEN MATCHED THEN UPDATE SET
  T.last_purchase_date = S.last_purchase_date,
  T.recency_days       = S.recency_days,
  T.frequency_orders   = S.frequency_orders,
  T.monetary_value     = S.monetary_value,
  T.churn_risk         = S.churn_risk,
  T.snapshot_date      = S.snapshot_date
WHEN NOT MATCHED BY TARGET THEN
  INSERT (customer_id, last_purchase_date, recency_days, frequency_orders, monetary_value, churn_risk, snapshot_date)
  VALUES (S.customer_id, S.last_purchase_date, S.recency_days, S.frequency_orders, S.monetary_value, S.churn_risk, S.snapshot_date);
