import pandas as pd

# Chemins vers les fichiers CSV à joindre
file1 = 'modis_2023_France.csv'
file2 = 'coordinates_updated3.csv'

# Charger les fichiers CSV dans des DataFrames pandas
df1 = pd.read_csv(file1)
df2 = pd.read_csv(file2)

# Fusionner les DataFrames sur les colonnes latitude, longitude et acq_time
merged_df = pd.merge(df1, df2, on=['latitude', 'longitude', 'acq_date'], how='inner')

# Chemin vers le fichier CSV de sortie
output_file = 'merged_coordinates.csv'

# Enregistrer le DataFrame fusionné dans un fichier CSV
merged_df.to_csv(output_file, index=False)

print(f'Fusion des fichiers CSV terminée. Résultat enregistré dans {output_file}')
