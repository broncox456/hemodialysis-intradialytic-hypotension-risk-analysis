from pathlib import Path
import pandas as pd
import numpy as np

INPUT_FILE = Path("data/processed/hd_clean.csv")
OUTPUT_DIR = Path("results/tables")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def build_score(row: pd.Series) -> int:
    score = 0

    if pd.notna(row.get("ufr_ml_kg_h")) and row["ufr_ml_kg_h"] > 10:
        score += 2
    if pd.notna(row.get("idwg_kg")) and row["idwg_kg"] > 3:
        score += 2
    if pd.notna(row.get("hb_gdl")) and row["hb_gdl"] < 10:
        score += 1
    if str(row.get("acceso_vascular", "")).upper() == "CATETER":
        score += 1
    if pd.notna(row.get("fevi_reducida")) and row["fevi_reducida"] == 1:
        score += 2
    if pd.notna(row.get("infeccion_3m")) and row["infeccion_3m"] == 1:
        score += 1

    return score


def categorize(score: int) -> str:
    if score <= 2:
        return "low"
    if score <= 5:
        return "moderate"
    return "high"


def main() -> None:
    if not INPUT_FILE.exists():
        raise FileNotFoundError("Primero ejecuta scripts/01_cleaning.py")

    df = pd.read_csv(INPUT_FILE)
    df["idh_risk_score"] = df.apply(build_score, axis=1)
    df["idh_risk_category"] = df["idh_risk_score"].apply(categorize)

    df.to_csv(OUTPUT_DIR / "07_hd_with_risk_score.csv", index=False, encoding="utf-8-sig")

    score_summary = df.groupby("idh_risk_category")["idh"].agg(["count", "sum", "mean"]).reset_index()
    score_summary.columns = ["idh_risk_category", "n", "idh_events", "idh_rate"]
    score_summary["idh_rate"] = score_summary["idh_rate"].round(4)
    score_summary.to_csv(OUTPUT_DIR / "08_risk_score_summary.csv", index=False, encoding="utf-8-sig")

    points_table = pd.DataFrame({
        "factor": [
            "UFR > 10 ml/kg/h",
            "IDWG > 3 kg",
            "Hemoglobin < 10 g/dL",
            "Catheter access",
            "Reduced FEVI",
            "Recent infection (3 months)"
        ],
        "points": [2, 2, 1, 1, 2, 1]
    })
    points_table.to_csv(OUTPUT_DIR / "09_risk_score_definition.csv", index=False, encoding="utf-8-sig")

    print("Risk score generated successfully in results/tables")


if __name__ == "__main__":
    main()
