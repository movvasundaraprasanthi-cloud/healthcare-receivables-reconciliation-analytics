from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

def test_required_project_outputs_exist():
    assert (ROOT / "data/raw").exists()
    assert (ROOT / "data/processed/analytical_detail.csv").exists()
    assert (ROOT / "data/exports/executive_kpi_summary.csv").exists()

def test_analytical_detail_has_rows_and_no_patient_phi_columns():
    df = pd.read_csv(ROOT / "data/processed/analytical_detail.csv")
    assert len(df) > 100
    forbidden = {"patient_name", "member_name", "ssn", "dob", "date_of_birth"}
    assert forbidden.isdisjoint({c.lower() for c in df.columns})

def test_kpi_summary_has_valid_numeric_values():
    df = pd.read_csv(ROOT / "data/exports/executive_kpi_summary.csv")
    assert len(df) > 0
    numeric = df.select_dtypes(include="number")
    assert not numeric.isna().all(axis=None)
