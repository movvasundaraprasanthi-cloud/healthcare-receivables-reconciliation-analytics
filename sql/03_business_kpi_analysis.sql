-- KPI analysis pattern using joins, aggregations, and trend logic.
WITH monthly AS (
    SELECT
        report_month,
        business_segment,
        COUNT(*) AS record_count,
        SUM(exception_flag) AS exception_count
    FROM analytics_fact
    GROUP BY report_month, business_segment
)
SELECT
    *,
    exception_count * 1.0 / NULLIF(record_count, 0) AS exception_rate,
    LAG(exception_count * 1.0 / NULLIF(record_count, 0)) OVER (
        PARTITION BY business_segment ORDER BY report_month
    ) AS prior_month_exception_rate
FROM monthly;
