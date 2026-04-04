from pathlib import Path
import pandas as pd

INPUT_FILE = Path("data/processed/hd_clean.csv")
OUTPUT_DIR = Path("results/tables")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def main() -> None:
    if not INPUT_FILE.exists():
        raise FileNotFoundError("Primero ejecuta scripts/01_cleaning.py")

    df = pd.read_csv(INPUT_FILE)

    # Resumen global
    global_summary = pd.DataFrame({
        "metric": [
            "n_sessions", "n_patients", "idh_events", "idh_rate",
            "mean_ufr", "mean_idwg", "mean_hb", "catheter_rate", "fevi_reduced_rate"
        ],
        "value": [
            len(df),
            df["id_paciente"].nunique() if "id_paciente" in df.columns else None,
            int(df["idh"].sum()) if "idh" in df.columns else None,
            round(df["idh"].mean(), 4) if "idh" in df.columns else None,
            round(df["ufr_ml_kg_h"].mean(), 2) if "ufr_ml_kg_h" in df.columns else None,
            round(df["idwg_kg"].mean(), 2) if "idwg_kg" in df.columns else None,
            round(df["hb_gdl"].mean(), 2) if "hb_gdl" in df.columns else None,
            round((df["acceso_vascular"].astype(str).str.upper() == "CATETER").mean(), 4) if "acceso_vascular" in df.columns else None,
            round(df["fevi_reducida"].mean(), 4) if "fevi_reducida" in df.columns else None,
        ]
    })
    global_summary.to_csv(OUTPUT_DIR / "00_global_summary.csv", index=False, encoding="utf-8-sig")

    # Resumen por IDH
    vars_by_idh = [c for c in [
        "ufr_ml_kg_h", "idwg_kg", "hb_gdl", "pam_pre", "pam_final", "delta_pam_90",
        "drop_sys_max", "bolo_salino", "pausa_uf", "fin_anticipado", "fevi_reducida", "infeccion_3m"
    ] if c in df.columns]

    summary_by_idh = df.groupby("idh")[vars_by_idh].agg(["mean", "median"]).round(2)
    summary_by_idh.to_csv(OUTPUT_DIR / "01_summary_by_idh.csv", encoding="utf-8-sig")

    # Tasas por factores clínicos
    if "acceso_vascular" in df.columns:
        access_idh = df.groupby("acceso_vascular", dropna=False)["idh"].agg(["count", "sum", "mean"]).reset_index()
        access_idh.columns = ["acceso_vascular", "n", "idh_events", "idh_rate"]
        access_idh["idh_rate"] = access_idh["idh_rate"].round(4)
        access_idh.to_csv(OUTPUT_DIR / "02_idh_by_access.csv", index=False, encoding="utf-8-sig")

    if "anemia_flag" in df.columns:
        anemia_idh = df.groupby("anemia_flag")["idh"].agg(["count", "sum", "mean"]).reset_index()
        anemia_idh.columns = ["anemia_flag", "n", "idh_events", "idh_rate"]
        anemia_idh["idh_rate"] = anemia_idh["idh_rate"].round(4)
        anemia_idh.to_csv(OUTPUT_DIR / "03_idh_by_anemia.csv", index=False, encoding="utf-8-sig")

    if "fevi_reducida" in df.columns:
        fevi_idh = df.groupby("fevi_reducida")["idh"].agg(["count", "sum", "mean"]).reset_index()
        fevi_idh.columns = ["fevi_reducida", "n", "idh_events", "idh_rate"]
        fevi_idh["idh_rate"] = fevi_idh["idh_rate"].round(4)
        fevi_idh.to_csv(OUTPUT_DIR / "04_idh_by_fevi.csv", index=False, encoding="utf-8-sig")

    if "infeccion_3m" in df.columns:
        inf_idh = df.groupby("infeccion_3m")["idh"].agg(["count", "sum", "mean"]).reset_index()
        inf_idh.columns = ["infeccion_3m", "n", "idh_events", "idh_rate"]
        inf_idh["idh_rate"] = inf_idh["idh_rate"].round(4)
        inf_idh.to_csv(OUTPUT_DIR / "05_idh_by_infection.csv", index=False, encoding="utf-8-sig")

    # Pacientes con mayor carga de IDH
    if {"id_paciente", "idh"}.issubset(df.columns):
        patient_burden = df.groupby("id_paciente")["idh"].agg(["count", "sum", "mean"]).reset_index()
        patient_burden.columns = ["id_paciente", "n_sessions", "idh_events", "idh_rate"]
        patient_burden = patient_burden.sort_values(["idh_events", "idh_rate"], ascending=False)
        patient_burden.to_csv(OUTPUT_DIR / "06_patient_idh_burden.csv", index=False, encoding="utf-8-sig")

    print("Analysis tables generated successfully in results/tables")


if __name__ == "__main__":
    main()
