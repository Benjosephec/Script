import csv
import os

# Fonction pour charger un fichier CSV
def load_csv(file_path):
    """Charge un fichier CSV et retourne son en-tête et les données sous forme de liste."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Le fichier n'existe pas.")
    
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader)  # Lecture de l'en-tête
        data = [row for row in reader]
    return header, data

# Fonction pour vérifier que les en-têtes de deux fichiers CSV sont identiques
def equality_check(header1, header2):
    """Vérifie que deux en-têtes de fichiers CSV sont identiques."""
    return header1 == header2

# Fonction pour rechercher un produit dans les données
def search_product(data, product_name):
    """Recherche un produit par son nom dans les données."""
    result = [row for row in data if row[0].lower() == product_name.lower()]
    return result

# Fonction pour générer un résumé des stocks (quantité totale et prix moyen par catégorie)
def generate_summary(data):
    """Génère un résumé par catégorie (quantité totale et prix moyen)."""
    summary = {}
    for row in data:
        category = row[3]  # Catégorie est dans la 4ème colonne
        quantity = float(row[1])  # Quantité est dans la 2ème colonne
        price = float(row[2])  # Prix unitaire est dans la 3ème colonne
        
        if category not in summary:
            summary[category] = {'total_quantity': 0, 'total_price': 0.0, 'count': 0}
        
        summary[category]['total_quantity'] += quantity
        summary[category]['total_price'] += price * quantity
        summary[category]['count'] += 1
    
    # Calcul du prix moyen par catégorie
    for category, stats in summary.items():
        avg_price = stats['total_price'] / stats['total_quantity'] if stats['total_quantity'] > 0 else 0
        stats['average_price'] = avg_price
    
    return summary

# Fonction pour trier les données par une colonne donnée
def sort_data(data, column_index, reverse=False):
    """Trie les données selon une colonne donnée, avec option pour inverser l'ordre."""

    def safe_convert(value):
        try:
            return float(value)
        except ValueError:
            return float('inf')  # Non-numeric values are treated as "infinity" to be sorted at the end

    try:
        # First sort by numeric values, then by non-numeric values.
        sorted_data = sorted(data, key=lambda row: (safe_convert(row[column_index]), row[column_index]),
                             reverse=reverse)
        return sorted_data
    except Exception as e:
        raise ValueError(f"Impossible de trier les données : {e}")

# Fonction pour exporter les données vers un fichier CSV
def export_data(file_path, data, header):
    """Exporte les données vers un fichier CSV."""
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(data)
