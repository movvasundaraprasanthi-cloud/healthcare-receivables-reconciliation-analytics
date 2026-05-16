# Validation Checklist

- [ ] Raw files exist in `data/raw/`.
- [ ] Processed files exist in `data/processed/`.
- [ ] BI exports exist in `data/exports/`.
- [ ] Required fields are populated.
- [ ] Business rules produce no invalid KPI values.
- [ ] Tests pass with `python -m pytest`.
- [ ] No PHI, SSNs, DOBs, or private data are present.
