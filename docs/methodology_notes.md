# Methodological Notes

This project was developed in staged steps:

1. Raw dialysis data extraction and cleaning
2. Feature engineering (UFR, IDWG, ΔMAP, IDH classification)
3. Exploratory statistical analysis
4. Risk score development
5. Patient-level aggregation and clustering

## Key Considerations

- IDH defined based on blood pressure drop and intervention signals
- Patient-level features derived from longitudinal aggregation
- Clustering performed using K-means (k=3)

## Limitations

- Single-center dataset
- Limited sample size
- Observational design