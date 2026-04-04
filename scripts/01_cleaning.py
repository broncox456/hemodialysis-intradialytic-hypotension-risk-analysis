import pandas as pd

# Cargar dataset desde Excel
df = pd.read_excel("data/raw/hd_marvesa.xlsx")

# Guardar número de filas inicial
raw_rows = len(df)

# Limpiar nombres de columnas
df.columns = df.columns.str.strip().str.lower()

# Eliminar duplicados
df = df.drop_duplicates()

# Convertir columnas clave a numérico
numeric_cols = ["edad", "hb_gdl", "ufr_ml_kg_h", "idwg_kg"]

for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# Eliminar filas con valores críticos faltantes
df = df.dropna(subset=["ufr_ml_kg_h", "idwg_kg", "hb_gdl"])

# Crear variable IDH binaria si no existe
if "idh" not in df.columns:
    if "probable_idh" in df.columns:
        df["idh"] = df["probable_idh"]
    else:
        df["idh"] = 0

# Guardar limpio
df.to_csv("data/processed/hd_clean.csv", index=False)

# Métricas
clean_rows = len(df)
n_patients = df["id_paciente"].nunique()
idh_rate = df["idh"].mean()

print("Cleaning completed successfully.")
print("Raw rows:", raw_rows)
print("Clean rows:", clean_rows)
print("Unique patients:", n_patients)
print("IDH rate:", round(idh_rate * 100, 2), "%")