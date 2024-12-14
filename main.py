import argparse
import os
from lib import combine_csv, search_data, generate_report, validate_csv


def parse_args():
    """Analyse les arguments de la ligne de commande."""
    parser = argparse.ArgumentParser(description="Gestion des stocks - Outil de commande")
    
    # Argument pour combiner les fichiers CSV
    parser.add_argument("--combine", nargs='+', help="Combiner des fichiers CSV en un seul fichier", required=False)
    
    # Argument pour rechercher des informations dans le fichier consolidé
    parser.add_argument("--search", nargs='+', help="Rechercher des informations par critères (clé valeur)", required=False)
    
    # Argument pour générer un rapport récapitulatif
    parser.add_argument("--report", help="Générer un rapport récapitulatif des stocks par catégorie", required=False)
    
    return parser.parse_args()


def combine_files(files):
    """Combine les fichiers CSV donnés en un seul fichier consolidé."""
    if len(files) < 2:
        print("Veuillez fournir au moins deux fichiers à combiner.")
        return
    output_file = "stocks_combine.csv"
    if all(validate_csv(file) for file in files):
        combine_csv(files, output_file)


def search_in_combined(criteria):
    """Effectue une recherche dans le fichier consolidé en fonction des critères fournis."""
    if not os.path.exists("stocks_combine.csv"):
        print("Le fichier combiné 'stocks_combine.csv' n'existe pas. Veuillez d'abord combiner les fichiers.")
        return
    criteria_dict = {criteria[i]: criteria[i + 1] for i in range(0, len(criteria), 2)}
    result = search_data("stocks_combine.csv", **criteria_dict)
    if not result.empty:
        print(result)
    else:
        print("Aucun résultat trouvé pour les critères spécifiés.")


def generate_summary_report():
    """Génère un rapport récapitulatif des stocks par catégorie."""
    if not os.path.exists("stocks_combine.csv"):
        print("Le fichier combiné 'stocks_combine.csv' n'existe pas. Veuillez d'abord combiner les fichiers.")
        return
    report_file = "rapport_stocks.csv"
    generate_report("stocks_combine.csv", report_file)


def main():
    """Fonction principale d'exécution."""
    args = parse_args()

    if args.combine:
        combine_files(args.combine)
    elif args.search:
        search_in_combined(args.search)
    elif args.report:
        generate_summary_report()
    else:
        print("Aucune option valide fournie. Utilisez --help pour plus d'informations.")


if __name__ == "__main__":
    main()
