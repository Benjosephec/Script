import argparse
from lib import load_csv, write_csv, merge_csv, sort_data


def main():
    parser = argparse.ArgumentParser(
        description="Programme pour manipuler des fichiers CSV : fusion, tri et export."
    )
    parser.add_argument(
        "file",
        nargs="+",
        help="Un ou plusieurs fichiers CSV à charger. Si plusieurs fichiers sont donnés, ils seront fusionnés.",
    )
    parser.add_argument(
        "-o", "--output",
        default=None,
        help="Nom du fichier CSV de sortie pour sauvegarder les résultats.",
    )
    parser.add_argument(
        "-s", "--sort",
        default=None,
        help="Nom de la colonne selon laquelle trier les données.",
    )
    parser.add_argument(
        "--force-overwrite",
        action="store_true",
        help="Forcer l'écrasement du fichier de sortie s'il existe déjà.",
    )

    args = parser.parse_args()

    # Vérification du fichier de sortie
    if args.output and not args.output.endswith(".csv"):
        raise ValueError("Le fichier de sortie doit avoir une extension .csv")

    data = []
    header = None

    # Charger et fusionner les fichiers
    if len(args.file) > 1:
        header, data = merge_csv(args.file, data, header)
    else:
        header, data = load_csv(args.file[0])

    # Trier les données si demandé
    if args.sort:
        try:
            data = sort_data(data, header, args.sort)
        except ValueError as e:
            print(f"Erreur lors du tri : {e}")
            return

    # Exporter ou afficher les résultats
    if args.output:
        write_csv(args.output, data, header, force_overwrite=args.force_overwrite)
        print(f"Les résultats ont été sauvegardés dans : {args.output}")
    else:
        print("En-têtes :", header)
        for row in data:
            print(row)


if __name__ == "__main__":
    main()
