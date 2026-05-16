from pathlib import Path
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"
EXPORTS = ROOT / "data" / "exports"
REPORTS = ROOT / "reports"

KIND = "receivables"

def read_csv(name):
    return pd.read_csv(RAW / f"{name}.csv")

def main():
    PROCESSED.mkdir(parents=True, exist_ok=True)
    EXPORTS.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    if KIND == "prior_auth":
        req, providers, products = read_csv("prior_authorization_requests"), read_csv("providers"), read_csv("payer_products")
        df = req.merge(providers, on="provider_id", how="left").merge(products, on="product_id", how="left")
        df["sla_met_flag"] = df["turnaround_hours"] <= df["sla_hours"]
        df["denied_flag"] = df["status"].eq("Denied")
        summary = df.groupby(["request_month","payer","line_of_business","specialty","network_status"], as_index=False).agg(request_count=("authorization_id","count"), denial_rate=("denied_flag","mean"), sla_met_rate=("sla_met_flag","mean"), avg_turnaround_hours=("turnaround_hours","mean"))
        detail = df
    elif KIND == "provider_quality":
        pm, cred, contracts, directory = read_csv("provider_master"), read_csv("credentialing_cases"), read_csv("provider_contracts"), read_csv("directory_records")
        df = pm.merge(cred, on="provider_id", how="left").merge(contracts, on="provider_id", how="left")
        df["invalid_npi_flag"] = df["npi"].isna() | (df["npi"].astype(str).str.len() != 10)
        df["duplicate_identity_flag"] = df.duplicated(["npi","tin"], keep=False) & df["npi"].notna()
        df["directory_complete_flag"] = df["directory_phone"].notna() & df["accepting_new_patients"].notna() & (df["last_update_days"] <= 120)
        df["quality_score"] = (100 - df.invalid_npi_flag.astype(int)*25 - df.duplicate_identity_flag.astype(int)*30 - (~df.directory_complete_flag).astype(int)*20 - df.credentialing_status.isin(["Expired","Pending"]).astype(int)*15).clip(lower=0)
        summary = df.groupby(["state","specialty","network_tier"], as_index=False).agg(provider_count=("provider_id","count"), avg_quality_score=("quality_score","mean"), duplicate_records=("duplicate_identity_flag","sum"), directory_completeness=("directory_complete_flag","mean"))
        detail = df
    elif KIND == "revops":
        tx, reps, terr, quota, disputes = read_csv("pos_transactions"), read_csv("sales_reps"), read_csv("territory_mapping"), read_csv("quota_plan"), read_csv("commission_disputes")
        df = tx.merge(reps, on="rep_id", how="left").merge(terr, on="territory_id", how="left", suffixes=("_rep","_territory")).merge(quota, on=["rep_id","sales_month"], how="left")
        df["missing_territory_flag"] = df["territory_id"].isna()
        df["duplicate_transaction_flag"] = df.duplicated(["rep_id","sales_month","net_revenue"], keep=False)
        df["commission_rate"] = np.where(df["net_revenue"] >= 10000, .08, .05)
        df["commission_amount"] = (df["net_revenue"] * df["commission_rate"]).round(2)
        summary = df.groupby(["sales_month","region_rep","manager"], as_index=False).agg(net_revenue=("net_revenue","sum"), quota_amount=("quota_amount","sum"), commission_amount=("commission_amount","sum"), exception_count=("missing_territory_flag","sum"))
        summary["quota_attainment"] = summary["net_revenue"] / summary["quota_amount"]
        detail = df
    elif KIND == "governance":
        systems, catalog, mappings, rules, rec = read_csv("source_systems"), read_csv("data_catalog"), read_csv("column_mappings"), read_csv("quality_rule_results"), read_csv("reconciliation_results")
        rec["variance"] = rec["target_count"] - rec["source_count"]
        rec["matched_flag"] = rec["variance"].abs() <= 5
        df = catalog.merge(systems, on="source_system", how="left")
        rule_summary = rules.groupby("table_name", as_index=False).agg(rule_count=("rule_id","count"), rule_pass_rate=("passed_flag","mean"), critical_failures=("severity", lambda s: int(((s == "Critical") & (~rules.loc[s.index, "passed_flag"])).sum())))
        df = df.merge(rule_summary, on="table_name", how="left")
        df["lineage_mapping_count"] = df["table_name"].map(mappings.source_table.value_counts()).fillna(0).astype(int)
        summary = df.groupby(["domain","steward","certification_status"], as_index=False).agg(table_count=("table_name","count"), avg_rule_pass_rate=("rule_pass_rate","mean"), lineage_mappings=("lineage_mapping_count","sum"))
        rec.to_csv(PROCESSED / "source_to_target_reconciliation.csv", index=False)
        detail = df
    else:
        claims, payments, postings, unapplied, adjustments = read_csv("pharmacy_claims"), read_csv("lockbox_payments"), read_csv("cash_postings"), read_csv("unapplied_cash"), read_csv("adjustment_recommendations")
        df = claims.merge(postings, on=["claim_id","client_id"], how="left")
        df["posting_exception_flag"] = df["posting_status"].fillna("Unposted").ne("Matched")
        df["variance_amount"] = (df["allowed_amount"] - df["posted_amount"].fillna(0)).round(2)
        summary = df.groupby(["service_month","client_id","claim_status"], as_index=False).agg(claim_count=("claim_id","count"), allowed_amount=("allowed_amount","sum"), posted_amount=("posted_amount","sum"), exception_count=("posting_exception_flag","sum"), variance_amount=("variance_amount","sum"))
        detail = df
        unapplied.to_csv(PROCESSED / "unapplied_cash_exceptions.csv", index=False)
        adjustments.to_csv(EXPORTS / "gl_adjustment_recommendations.csv", index=False)
    summary = summary.round(4)
    detail.to_csv(PROCESSED / "analytical_detail.csv", index=False)
    summary.to_csv(EXPORTS / "executive_kpi_summary.csv", index=False)
    detail.head(1000).to_csv(EXPORTS / "dashboard_detail_extract.csv", index=False)
    report = ["# Stakeholder Summary", "", "Generated from synthetic data. No PHI or private data is included.", "", f"Rows in analytical detail: {len(detail)}", f"Rows in KPI summary: {len(summary)}"]
    (REPORTS / "stakeholder_summary.md").write_text("\n".join(report), encoding="utf-8")

if __name__ == "__main__":
    main()
