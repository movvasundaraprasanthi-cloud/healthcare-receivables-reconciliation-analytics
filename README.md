# Healthcare Receivables Reconciliation Analytics

    ** Healthcare finance operations project reconciling prescription claims, lockbox payments, cash posting, unapplied cash, contractual adjustments, rebilling candidates, and client reporting outputs.

    ## Business Problem
    Organizations need reliable analytics that connect operational activity, data quality, exceptions, and stakeholder-ready KPIs. This project simulates Healthcare prescription receivables, unapplied cash, claims/cash posting, reconciliation, and client reporting using realistic synthetic data and production-style analytics assets.

    ## Business Impact
    - Classified unapplied cash and reconciliation exceptions for weekly client reporting.
    - Identified rebilling candidates and GL adjustment recommendations.
    - Created monthly finance operations exports for stakeholder review.

    ## Architecture
    ```text
    data/raw -> Python validation and analysis -> data/processed -> data/exports -> BI dashboard / stakeholder report
                 SQL scripts document warehouse transformations, validation rules, window functions, and KPI logic
    ```

    ## Tools Used
    SQL, Python, pandas, NumPy, pytest, Excel-ready CSVs, Power BI/Tableau-ready exports, Markdown documentation.

    ## Dataset
    All datasets are synthetic and safe for public GitHub. No PHI, patient names, SSNs, DOBs, or private data are included.

    Source tables:
    - `pharmacy_claims.csv`
- `lockbox_payments.csv`
- `cash_postings.csv`
- `unapplied_cash.csv`
- `adjustment_recommendations.csv`

    ## KPIs
    - Cash application rate
- Unapplied cash amount
- Reconciliation variance
- Rebilling candidate value
- Adjustment amount
- Client reporting completeness

    ## Business Insights
    - Exceptions are concentrated in specific operational segments, which enables targeted remediation instead of broad manual review.
    - SLA and quality metrics are more actionable when segmented by owner, product, provider, territory, client, or source system.
    - Reconciliation and duplicate detection reduce downstream reporting risk before executive dashboards are published.
    - BI-ready exports let analysts move quickly from validated data to stakeholder-facing dashboards.

    ## Dashboard Screenshots
    Add Power BI or Tableau screenshots to `dashboards/screenshots/`.

    ## Repository Structure
    ```text
    README.md
    data/raw
    data/processed
    data/exports
    sql
    src
    notebooks
    dashboards
    docs
    tests
    reports
    ```

    ## How to Run
    ```bash
    pip install -r requirements.txt
    python src/build_outputs.py
    python -m pytest
    ```

    ## Recruiter Keywords
    Receivables, reconciliation, unapplied cash, claims posting, GAAP, transaction analysis, Excel, SQL, client reporting, process improvement, healthcare finance operations

    ## Resume Bullet Points
    - Built a production-style Healthcare prescription receivables, unapplied cash, claims/cash posting, reconciliation, and client reporting analytics project using SQL, Python, pandas, automated validation checks, and BI-ready exports.
    - Developed SQL logic with joins, CTEs, window functions, aggregations, validation rules, exception tracking, and KPI reporting.
    - Automated data quality checks and stakeholder exports with pandas, including processed analytical details and executive KPI summaries.
    - Documented business requirements, KPI definitions, data dictionary, assumptions, validation checklist, dashboard plan, and stakeholder summary.

    ## Interview Talking Points
    - How claims, lockbox payments, and postings are reconciled.
- How unapplied cash categories are assigned.
- How rebilling candidates are detected.
- How GAAP-style adjustment recommendations are documented.
- How client-ready reporting packages are produced.
