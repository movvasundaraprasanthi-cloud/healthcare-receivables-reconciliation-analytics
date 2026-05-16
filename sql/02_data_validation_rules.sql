-- Data validation rules with CTEs and aggregations.
WITH profile AS (
    SELECT 'required_field_check' AS rule_name, COUNT(*) AS record_count
    FROM analytical_detail
)
SELECT rule_name, record_count FROM profile;
