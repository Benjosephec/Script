import os
import argparse
from lib import consolider_csv, rechercher_produit, generer_rapport

def main():
    parser = argparse.ArgumentParser(description="Gestion d'inventaire en ligne de commande")
    
    parser.add_argument("--consolider", help="Consolider les fichiers CSV dans un fichier unique", action="store_true")
    parser.add_argument("--rechercher", help="Rechercher des produits", action="store_true")
    parser.add_argument("--rapport", help="Générer un rapport récapitulatif", type=str)
    
    args = parser.parse_args()
    
    if args.consolider:
        chemin = "data"
        fichier_consolide = "output/inventaire_consolide.csv"
        consolider_csv(chemin, fichier_consolide)
        print(f"Consolidation terminée : {fichier_consolide}")
    
    elif args.rechercher:
        fichier = "output/inventaire_consolide.csv"
        if not os.path.exists(fichier):
            print(f"Le fichier consolidé {fichier} n'existe pas. Veuillez d'abord exécuter --consolider.")
        else:
            recherche = input("Entrez un critère de recherche (nom, catégorie ou prix) : ")
            resultats = rechercher_produit(fichier, recherche)
            if resultats.empty:
                print("Aucun résultat trouvé.")
            else:
                print(resultats)
    
    elif args.rapport:
        fichier = "output/inventaire_consolide.csv"
        if not os.path.exists(fichier):
            print(f"Le fichier consolidé {fichier} n'existe pas. Veuillez d'abord exécuter --consolider.")
        else:
            generer_rapport(fichier, args.rapport)
            print(f"Rapport généré : {args.rapport}")
    else:
        print("Aucune action spécifiée. Utilisez --help pour les options disponibles.")

if __name__ == "__main__":
    main()
