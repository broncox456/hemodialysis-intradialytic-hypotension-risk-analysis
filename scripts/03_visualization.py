from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

INPUT_FILE = Path("data/processed/hd_clean.csv")
OUTPUT_DIR = Path("results/figures")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def save_boxplot(df: pd.DataFrame, y: str, title: str, filename: str) -> None:
    fig, ax = plt.subplots(figsize=(7, 5))
    data0 = df.loc[df["idh"] == 0, y].dropna()
    data1 = df.loc[df["idh"] == 1, y].dropna()
    ax.boxplot([data0, data1], tick_labels=["No IDH", "IDH"])
    ax.set_title(title)
    ax.set_xlabel("Intradialytic hypotension")
    ax.set_ylabel(y)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / filename, dpi=300)
    plt.close(fig)


def save_bar_rate(df: pd.DataFrame, col: str, title: str, filename: str) -> None:
    temp = df.groupby(col)["idh"].mean().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(7, 5))
    temp.plot(kind="bar", ax=ax)
    ax.set_title(title)
    ax.set_xlabel(col)
    ax.set_ylabel("IDH rate")
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / filename, dpi=300)
    plt.close(fig)


def main() -> None:
    if not INPUT_FILE.exists():
        raise FileNotFoundError("Primero ejecuta scripts/01_cleaning.py")

    df = pd.read_csv(INPUT_FILE)

    if {"idh", "ufr_ml_kg_h"}.issubset(df.columns):
        save_boxplot(df, "ufr_ml_kg_h", "UFR by IDH", "01_ufr_by_idh.png")

    if {"idh", "idwg_kg"}.issubset(df.columns):
        save_boxplot(df, "idwg_kg", "IDWG by IDH", "02_idwg_by_idh.png")

    if {"idh", "hb_gdl"}.issubset(df.columns):
        save_boxplot(df, "hb_gdl", "Hemoglobin by IDH", "03_hb_by_idh.png")

    if {"idh", "delta_pam_90"}.issubset(df.columns):
        save_boxplot(df, "delta_pam_90", "Delta PAM 90 min by IDH", "04_delta_pam90_by_idh.png")

    if {"idh", "acceso_vascular"}.issubset(df.columns):
        save_bar_rate(df, "acceso_vascular", "IDH rate by vascular access", "05_idh_rate_by_access.png")

    if {"idh", "anemia_flag"}.issubset(df.columns):
        save_bar_rate(df, "anemia_flag", "IDH rate by anemia status", "06_idh_rate_by_anemia.png")

    if {"idh", "fevi_reducida"}.issubset(df.columns):
        save_bar_rate(df, "fevi_reducida", "IDH rate by reduced FEVI", "07_idh_rate_by_fevi.png")

    if {"idh", "infeccion_3m"}.issubset(df.columns):
        save_bar_rate(df, "infeccion_3m", "IDH rate by recent infection", "08_idh_rate_by_infection.png")

    print("Figures generated successfully in results/figures")


if __name__ == "__main__":
    main()
