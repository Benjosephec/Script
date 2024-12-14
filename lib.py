import pandas as pd
import os


def combine_csv(file_paths, output_file):
    """Combine plusieurs fichiers CSV en un seul fichier consolidé."""
    try:
        # Chargement et concaténation des fichiers CSV
        dataframes = [pd.read_csv(file) for file in file_paths]
        combined_df = pd.concat(dataframes, ignore_index=True)
        combined_df.to_csv(output_file, index=False)
        print(f"Fichiers combinés et exportés vers {output_file}")
    except Exception as e:
        print(f"Erreur lors de la combinaison des fichiers : {e}")


def search_data(csv_file, **criteria):
    """Recherche dans un fichier CSV en fonction de critères passés sous forme de mots-clés."""
    try:
        # Chargement du fichier CSV
        df = pd.read_csv(csv_file)
        for key, value in criteria.items():
            if key not in df.columns:
                print(f"Colonne '{key}' non trouvée dans les données.")
                return pd.DataFrame()  # Retourner un DataFrame vide
            df = df[df[key].str.contains(value, case=False, na=False)]
        return df
    except Exception as e:
        print(f"Erreur lors de la recherche : {e}")
        return pd.DataFrame()


def generate_report(csv_file, report_file):
    """Génère un rapport agrégé des stocks par catégorie et exporte en CSV."""
    try:
        # Chargement du fichier CSV
        df = pd.read_csv(csv_file)
        # Agrégation des données par catégorie
        report = df.groupby('categorie').agg({
            'quantite': 'sum',
            'prix_unitaire': 'mean',
            'nom': 'count'
        }).reset_index()
        # Export du rapport
        report.to_csv(report_file, index=False)
        print(f"Rapport généré et exporté vers {report_file}")
    except Exception as e:
        print(f"Erreur lors de la génération du rapport : {e}")


def validate_csv(file_path):
    """Vérifie si un fichier CSV est valide."""
    if not os.path.exists(file_path):
        print(f"Le fichier {file_path} n'existe pas.")
        return False
    try:
        # Tentative de chargement du fichier
        pd.read_csv(file_path)
        return True
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier {file_path} : {e}")
        return False
