
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# cargar data limpia
df = pd.read_csv("data/processed/hd_clean.csv")

# agrupar por paciente
patient = df.groupby("id_paciente").agg({
    "idh": "mean",
    "delta_pam_90": "mean",
    "drop_sys_max": "mean",
    "ufr_ml_kg_h": "mean",
    "bolo_salino": "mean"
}).reset_index()

patient.columns = [
    "patient_id",
    "idh_rate",
    "mean_delta_pam",
    "mean_drop_sys",
    "mean_ufr",
    "saline_use"
]

# llenar faltantes
patient = patient.fillna(0)

# variables para clustering
features = [
    "idh_rate",
    "mean_delta_pam",
    "mean_drop_sys",
    "mean_ufr",
    "saline_use"
]

X = patient[features]

# clustering
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
patient["cluster"] = kmeans.fit_predict(X)

# guardar tabla principal
patient.to_csv("results/tables/10_patient_clusters.csv", index=False)

# resumen por cluster: solo columnas numéricas
cluster_summary = patient.groupby("cluster")[features].agg(["mean", "median"])
cluster_summary.to_csv("results/tables/11_cluster_summary.csv")

print("Clustering completed successfully.")
print(patient["cluster"].value_counts().sort_index())

# figura
plt.figure(figsize=(8, 6))
plt.scatter(patient["idh_rate"], patient["mean_drop_sys"], c=patient["cluster"])
plt.xlabel("IDH rate")
plt.ylabel("Mean drop in systolic BP")
plt.title("Patient clusters by intradialytic instability")
plt.savefig("results/figures/patient_clusters.png", bbox_inches="tight")
plt.close()