import os
import csv


def load_csv(file: str, delimiter: str = ",") -> tuple[list[str], list[list[str]]]:
    """
    Charge un fichier CSV en mémoire.
    Retourne une liste représentant l'en-tête et une liste des lignes de données.
    """
    if not os.path.exists(file):
        raise FileNotFoundError(f"Le fichier {file} est introuvable.")

    with open(file, newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile, delimiter=delimiter)
        rows = list(reader)
        if not rows:
            raise ValueError(f"Le fichier {file} est vide.")
        header = rows[0]  # La première ligne contient les en-têtes
        data = rows[1:]   # Les lignes suivantes contiennent les données
        return header, data


def write_csv(
    file: str, data: list[list[str]], header: list[str], force_overwrite: bool = False
) -> None:
    """
    Écrit les données dans un fichier CSV, avec un contrôle d'écrasement optionnel.
    """
    if not force_overwrite and os.path.exists(file):
        choix = input(
            f"Attention : le fichier {file} existe déjà. Voulez-vous l'écraser ? (yes/n) "
        )
        if choix.lower() != "yes":
            print("Écriture annulée.")
            return

    with open(file, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        writer.writerows(data)
    print(f"Fichier {file} écrit avec succès.")


def merge_csv(files: list[str], data: list[list[str]], header: list[str]) -> tuple[list[str], list[list[str]]]:
    """
    Fusionne plusieurs fichiers CSV en validant les en-têtes.
    """
    for file in files:
        file_header, file_data = load_csv(file)
        if header is None:
            header = file_header
        elif header != file_header:
            raise ValueError(f"Les en-têtes ne correspondent pas dans le fichier : {file}")
        data.extend(file_data)
    return header, data


def sort_data(data: list[list[str]], header: list[str], column: str, reverse: bool = False) -> list[list[str]]:
    """
    Trie les données d'un fichier CSV par une colonne donnée.
    """
    if column not in header:
        raise ValueError(f"La colonne '{column}' n'existe pas.")
    col_index = header.index(column)
    try:
        return sorted(data, key=lambda x: float(x[col_index]) if x[col_index].replace('.', '', 1).isdigit() else x[col_index], reverse=reverse)
    except Exception as e:
        raise ValueError(f"Impossible de trier par la colonne '{column}': {e}")
