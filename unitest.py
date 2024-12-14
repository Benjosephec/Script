import unittest
import os
from io import StringIO
from lib import load_csv, search_product, generate_summary, sort_data, export_data

class TestCSVStockManager(unittest.TestCase):

    def setUp(self):
        # Création d'un fichier CSV temporaire pour les tests
        self.test_file = "test_inventory.csv"
        self.test_data = """product_name,quantity,unit_price,category
Laptop,10,800.0,Electronics
Smartphone,15,500.0,Electronics
Wireless Mouse,8,25.0,Accessories
"""
        with open(self.test_file, 'w') as f:
            f.write(self.test_data)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    # Test de la fonction load_csv avec un fichier valide
    def test_load_csv(self):
        header, data = load_csv(self.test_file)
        self.assertEqual(header, ['product_name', 'quantity', 'unit_price', 'category'])
        self.assertEqual(len(data), 3)
        self.assertEqual(data[0], ['Laptop', '10', '800.0', 'Electronics'])

    # Test du fichier CSV vide (pas de données)
    def test_load_empty_csv(self):
        empty_file = "empty_inventory.csv"
        with open(empty_file, 'w') as f:
            f.write("")
        header, data = load_csv(empty_file)
        self.assertEqual(header, [])
        self.assertEqual(data, [])
        os.remove(empty_file)

    # Test du fichier CSV avec des en-têtes différentes
    def test_load_csv_with_different_headers(self):
        invalid_file = "invalid_inventory.csv"
        invalid_data = """item_name,quantity,price,group
Laptop,10,800.0,Electronics
"""
        with open(invalid_file, 'w') as f:
            f.write(invalid_data)
        with self.assertRaises(ValueError):
            load_csv(invalid_file)
        os.remove(invalid_file)

    # Test de la recherche d'un produit existant
    def test_search_product_found(self):
        header, data = load_csv(self.test_file)
        result = search_product(data, "Laptop")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], ['Laptop', '10', '800.0', 'Electronics'])

    # Test de la recherche d'un produit inexistant
    def test_search_product_not_found(self):
        header, data = load_csv(self.test_file)
        result = search_product(data, "Tablet")
        self.assertEqual(len(result), 0)

    # Test de la génération du résumé des catégories
    def test_generate_summary(self):
        header, data = load_csv(self.test_file)
        summary = generate_summary(data)
        self.assertEqual(summary['Electronics']['total_quantity'], 25)
        self.assertEqual(summary['Electronics']['average_price'], 650.0)
        self.assertEqual(summary['Accessories']['total_quantity'], 8)

    # Test de la génération d'un résumé avec une catégorie manquante
    def test_generate_summary_category_missing(self):
        missing_category_data = """product_name,quantity,unit_price,category
Laptop,10,800.0,Electronics
Smartphone,15,500.0,Electronics
"""
        header, data = load_csv(StringIO(missing_category_data))
        summary = generate_summary(data)
        self.assertEqual(len(summary), 1)  # Seulement une catégorie 'Electronics'
        self.assertIn('Electronics', summary)
        self.assertNotIn('Accessories', summary)

    # Test du tri des données par prix unitaire, ordre croissant
    def test_sort_data_ascending(self):
        header, data = load_csv(self.test_file)
        sorted_data = sort_data(data, 2, reverse=False)  # Tri par prix unitaire
        self.assertEqual(sorted_data[0][0], 'Wireless Mouse')  # Le prix le plus bas
        self.assertEqual(sorted_data[-1][0], 'Laptop')  # Le prix le plus élevé

    # Test du tri des données par prix unitaire, ordre décroissant
    def test_sort_data_descending(self):
        header, data = load_csv(self.test_file)
        sorted_data = sort_data(data, 2, reverse=True)  # Tri par prix unitaire
        self.assertEqual(sorted_data[0][0], 'Laptop')  # Le prix le plus élevé
        self.assertEqual(sorted_data[-1][0], 'Wireless Mouse')  # Le prix le plus bas

    # Test de l'exportation des données vers un fichier CSV
    def test_export_data(self):
        header, data = load_csv(self.test_file)
        output_file = "exported_inventory.csv"
        export_data(output_file, data, header)
        self.assertTrue(os.path.exists(output_file))
        # Vérifier que le contenu du fichier exporté est correct
        with open(output_file, 'r') as f:
            exported_data = f.read()
            self.assertIn("Laptop", exported_data)
            self.assertIn("Smartphone", exported_data)
        os.remove(output_file)

    # Test d'exportation sans données
    def test_export_empty_data(self):
        empty_file = "empty_inventory.csv"
        with open(empty_file, 'w') as f:
            f.write("product_name,quantity,unit_price,category\n")
        header, data = load_csv(empty_file)
        output_file = "export_empty_inventory.csv"
        export_data(output_file, data, header)
        self.assertTrue(os.path.exists(output_file))
        with open(output_file, 'r') as f:
            exported_data = f.read()
            self.assertEqual(exported_data, "product_name,quantity,unit_price,category\n")
        os.remove(output_file)

    # Test du cas où les prix ou les quantités sont non numériques
    def test_invalid_quantity_and_price(self):
        invalid_data = """product_name,quantity,unit_price,category
Laptop,invalid,800.0,Electronics
Smartphone,15,invalid,Electronics
"""
        invalid_file = "invalid_values_inventory.csv"
        with open(invalid_file, 'w') as f:
            f.write(invalid_data)
        with self.assertRaises(ValueError):
            load_csv(invalid_file)
        os.remove(invalid_file)

    # Test avec un grand nombre de produits
    def test_large_inventory(self):
        large_data = "product_name,quantity,unit_price,category\n"
        for i in range(10000):
            large_data += f"Product{i},10,{i*5},Category\n"
        large_file = "large_inventory.csv"
        with open(large_file, 'w') as f:
            f.write(large_data)
        header, data = load_csv(large_file)
        self.assertEqual(len(data), 10000)
        os.remove(large_file)

    # Test des cas où des colonnes attendues sont manquantes
    def test_missing_column(self):
        invalid_data = """product_name,quantity,category
Laptop,10,Electronics
Smartphone,15,Electronics
"""
        invalid_file = "missing_column_inventory.csv"
        with open(invalid_file, 'w') as f:
            f.write(invalid_data)
        with self.assertRaises(ValueError):
            load_csv(invalid_file)
        os.remove(invalid_file)

    # Test de la gestion des données de type incohérents (quantité dans un champ non numérique)
    def test_inconsistent_data_type(self):
        inconsistent_data = """product_name,quantity,unit_price,category
Laptop,10,800.0,Electronics
Smartphone,text,500.0,Electronics
"""
        inconsistent_file = "inconsistent_data_inventory.csv"
        with open(inconsistent_file, 'w') as f:
            f.write(inconsistent_data)
        header, data = load_csv(inconsistent_file)
        self.assertRaises(ValueError)  # Attente d'une erreur de type
        os.remove(inconsistent_file)

if __name__ == '__main__':
    unittest.main()
