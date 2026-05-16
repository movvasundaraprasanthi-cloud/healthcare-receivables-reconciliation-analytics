-- Window-function pattern for prioritizing operational exceptions.
WITH ranked AS (
    SELECT
        *,
        ROW_NUMBER() OVER (PARTITION BY business_owner ORDER BY risk_score DESC) AS risk_rank,
        AVG(risk_score) OVER (PARTITION BY business_owner) AS owner_avg_risk_score
    FROM exception_worklist
)
SELECT * FROM ranked WHERE risk_rank <= 25;
