import unittest
from lib import *


class TestInventoryManager(unittest.TestCase):

    def test_load_csv_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            load_csv("data/non_existing_file.csv")

    # Test for load_csv with a real CSV file in the /data directory
    def test_load_csv_valid(self):
        file_path = 'data/test.csv'  # Ensure this file exists in the /data folder
        header, data = load_csv(file_path)

        # Check that the header is as expected
        self.assertEqual(header, ["Product", "Quantity", "Price", "Category"])

        # Check that the data is as expected
        self.assertEqual(data, [
            ["ProductA", "10", "20.5", "Category1"],
            ["ProductB", "5", "30.0", "Category2"]
        ])

    # Test for search_product with case-insensitivity
    def test_search_product_case_insensitivity(self):
        data = [
            ["ProductA", "10", "20.5", "Category1"],
            ["productb", "5", "30.0", "Category2"],
            ["ProDuctC", "15", "25.0", "Category1"]
        ]
        result = search_product(data, "PRODUCTA")
        self.assertEqual(result, [["ProductA", "10", "20.5", "Category1"]])

        result = search_product(data, "productB")
        self.assertEqual(result, [["productb", "5", "30.0", "Category2"]])

    # Test for generate_summary with non-numeric quantity or price
    def test_generate_summary_non_numeric_values(self):
        data = [
            ["ProductA", "10", "20.5", "Category1"],
            ["ProductB", "five", "30.0", "Category2"],  # Invalid quantity "five"
            ["ProductC", "15", "NaN", "Category1"],  # Invalid price "NaN"
        ]
        with self.assertRaises(ValueError):
            generate_summary(data)

    # Test for export_data with a file path that already exists
    def test_export_data(self):
        data = [
            ["ProductA", "10", "20.5", "Category1"],
            ["ProductB", "5", "30.0", "Category2"]
        ]
        header = ["Product", "Quantity", "Price", "Category"]

        # Use the export function to save the data in a new file
        export_data("output.csv", data, header)

        # After exporting, verify the file exists and check its contents
        self.assertTrue(os.path.exists("output.csv"))

        with open("output.csv", mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            file_header = next(reader)
            self.assertEqual(file_header, header)

            # Read and check the content of the CSV
            file_data = list(reader)
            self.assertEqual(file_data, data)

    # Test for load_csv when the file is empty but still exists (only header)
    def test_load_csv_empty_file_with_header(self):
        file_path = 'data/empty_file_with_header.csv'  # This file should exist in the /data folder
        header, data = load_csv(file_path)
        self.assertEqual(header, ["Product", "Quantity", "Price", "Category"])
        self.assertEqual(data, [])

    # Test for generate_summary with a single category and product
    def test_generate_summary_single_category(self):
        data = [
            ["ProductA", "10", "20.5", "Category1"],
            ["ProductB", "5", "30.0", "Category1"]
        ]
        summary = generate_summary(data)
        self.assertEqual(summary["Category1"]["total_quantity"], 15)
        self.assertAlmostEqual(summary["Category1"]["average_price"], 23.67, places=2)

    # Test for sorting non-numeric values with numbers
    def test_sort_data_non_numeric_sort(self):
        data = [
            ["ProductA", "10", "Twenty", "Category1"],
            ["ProductB", "5", "Thirty", "Category2"],
            ["ProductC", "15", "Ten", "Category1"]
        ]
        # Sorting by price (alphabetically)
        sorted_data = sort_data(data, 2)  # Sorting by price

        # After sorting, we expect numeric prices to be before non-numeric values
        self.assertEqual(sorted_data[0], ["ProductC", "15", "Ten", "Category1"])  # "Ten" comes first

    # Test for sorting with string in numeric column
    def test_sort_data_with_string_in_numeric_column(self):
        data = [
            ["ProductA", "10", "20.5", "Category1"],
            ["ProductB", "5", "NaN", "Category2"],  # Invalid price "NaN"
            ["ProductC", "15", "25.0", "Category1"]
        ]
        sorted_data = sort_data(data, 2)  # Sorting by price (which contains invalid values)

        # After sorting, we expect the invalid "NaN" to be at the end of the list
        self.assertEqual(sorted_data[0], ["ProductA", "10", "20.5", "Category1"])


if __name__ == '__main__':
    unittest.main()
