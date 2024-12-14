import os
from lib import load_csv, search_product, generate_summary, sort_data, export_data, equality_check

def main():
    inventory_data = []
    header = []
    
    while True:
        print("\nBienvenue dans le gestionnaire d'inventaire")
        print("1. Charger un fichier CSV")
        print("2. Rechercher un produit")
        print("3. Générer un résumé par catégorie")
        print("4. Trier les données")
        print("5. Exporter les données")
        print("6. Afficher les données")
        print("7. Quitter")
        
        choice = input("Choisissez une option : ")

        if choice == "1":
            # Charger les fichiers CSV
            folder = input("Entrez le chemin du dossier contenant les fichiers CSV : ")
            try:
                files = [f for f in os.listdir(folder) if f.endswith('.csv')]
                if not files:
                    print(f"Aucun fichier CSV trouvé dans le dossier {folder}")
                    continue
                for file in files:
                    file_path = os.path.join(folder, file)
                    print(f"Chargement de {file_path}...")
                    new_header, new_data = load_csv(file_path)
                    
                    if header and not equality_check(header, new_header):
                        print(f"Les en-têtes du fichier {file} ne correspondent. Ignoré.")
                        continue
                    
                    if not header:
                        header = new_header
                    inventory_data.extend(new_data)
                print("Fichiers CSV chargés avec succès.")
            except FileNotFoundError as e:
                print(e)

        elif choice == "2":
            # Recherche d'un produit
            product_name = input("Entrez le nom du produit à rechercher : ")
            found_products = search_product(inventory_data, product_name)
            if found_products:
                print("Produit(s) trouvé(s) :")
                for product in found_products:
                    print(product)
            else:
                print("Aucun produit trouvé.")

        elif choice == "3":
            # Générer un résumé des stocks par catégorie
            summary = generate_summary(inventory_data)
            print("Résumé des stocks par catégorie :")
            for category, stats in summary.items():
                print(f"{category}: Quantité totale = {stats['total_quantity']}, Prix moyen = {stats['average_price']:.2f}")

        elif choice == "4":
            # Trier les données
            print("1. Trier par produit")
            print("2. Trier par quantité")
            print("3. Trier par prix unitaire")
            column_choice = input("Choisissez la colonne pour trier : ")
            reverse_choice = input("Trier dans l'ordre inverse (o/n) ? : ")

            reverse = reverse_choice.lower() == "o"

            if column_choice == "1":
                sorted_data = sort_data(inventory_data, 0, reverse)  # Trier par produit
            elif column_choice == "2":
                sorted_data = sort_data(inventory_data, 1, reverse)  # Trier par quantité
            elif column_choice == "3":
                sorted_data = sort_data(inventory_data, 2, reverse)  # Trier par prix
            else:
                print("Choix invalide.")
                continue

            print("Données triées avec succès.")
            inventory_data = sorted_data

        elif choice == "5":
            # Exporter les données dans un fichier CSV
            export_path = input("Entrez le nom du fichier d'export (ex. export.csv) : ")
            export_data(export_path, inventory_data, header)
            print(f"Données exportées dans {export_path}.")

        elif choice == "6":
            # Afficher les données
            if not inventory_data:
                print("Aucune donnée à afficher.")
            else:
                print(f"\n{header}")
                for row in inventory_data:
                    print(row)

        elif choice == "7":
            # Quitter le programme
            print("Au revoir !")
            break

        else:
            print("Option invalide. Veuillez réessayer.")

if __name__ == "__main__":
    main()
