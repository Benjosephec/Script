import pandas as pd
import os

def consolider_csv(chemin_dossier, fichier_sortie):
    """Consolide tous les fichiers CSV d'un dossier en un seul fichier."""
    fichiers = [os.path.join(chemin_dossier, f) for f in os.listdir(chemin_dossier) if f.endswith('.csv')]
    if not fichiers:
        print("Aucun fichier CSV trouvé.")
        return
    
    donnees = []
    for fichier in fichiers:
        df = pd.read_csv(fichier)
        donnees.append(df)
    
    df_consolide = pd.concat(donnees, ignore_index=True)
    df_consolide.to_csv(fichier_sortie, index=False)

def rechercher_produit(fichier_csv, critere):
    """Recherche des produits selon un critère."""
    df = pd.read_csv(fichier_csv)
    return df[df.apply(lambda row: critere.lower() in row.to_string().lower(), axis=1)]

def generer_rapport(fichier_csv, fichier_rapport):
    """Génère un rapport récapitulatif des données."""
    df = pd.read_csv(fichier_csv)
    
    rapport = {
        "Nombre total de produits": len(df),
        "Quantité totale": df["Quantité"].sum(),
        "Valeur totale (en €)": (df["Quantité"] * df["Prix Unitaire"]).sum(),
        "Répartition par catégorie": df.groupby("Catégorie")["Quantité"].sum().to_dict()
    }
    
    with open(fichier_rapport, "w") as f:
        for cle, valeur in rapport.items():
            f.write(f"{cle}: {valeur}\n")
