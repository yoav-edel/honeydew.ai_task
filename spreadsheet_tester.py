import unittest
from spreadsheet import Spreadsheet
from erros import CircularReferenceError
from utills import Utills


class TestSpreadsheet(unittest.TestCase):
    """Unit tests for the Spreadsheet evaluator."""

    def test_basic_numbers_and_empty(self):
        """Test evaluation with basic numbers and empty cells."""
        data = [
            ["1", "2", ""],
            ["", "3", "4"]
        ]
        expected = [
            [1, 2, 0],
            [0, 3, 4]
        ]
        sheet = Spreadsheet(data)
        result = sheet.evaluate()
        self.assertEqual(result, expected)

    def test_simple_references(self):
        """Test cells that simply reference other cells."""
        data = [
            ["1", "2", "3"],
            ["=A1", "=B1", "=C1"],
        ]
        expected = [
            [1, 2, 3],
            [1, 2, 3]
        ]
        sheet = Spreadsheet(data)
        result = sheet.evaluate()
        self.assertEqual(result, expected)

    def test_formula_arithmetic(self):
        """Test formulas with basic arithmetic operations."""
        data = [
            ["10", "20", ""],
            ["=A1+5", "=B1-10", "=A1+B1"]
        ]
        expected = [
            [10, 20, 0],
            [15, 10, 30]
        ]
        sheet = Spreadsheet(data)
        result = sheet.evaluate()
        self.assertEqual(result, expected)

    def test_chained_references(self):
        """Test cells that reference other cells in a chain."""
        data = [
            ["1", "=A1+1", "=B1+1"]
        ]
        expected = [
            [1, 2, 3]
        ]
        sheet = Spreadsheet(data)
        result = sheet.evaluate()
        self.assertEqual(result, expected)

    def test_circular_reference_direct(self):
        """Test detection of direct circular references."""
        data = [
            ["=A1"]
        ]
        sheet = Spreadsheet(data)
        with self.assertRaises(CircularReferenceError):
            sheet.evaluate()

    def test_circular_reference_indirect(self):
        """Test detection of indirect circular references."""
        data = [
            ["=B1", "=A1"]
        ]
        sheet = Spreadsheet(data)
        with self.assertRaises(CircularReferenceError):
            sheet.evaluate()

    def test_circular_reference_long_cycle(self):
        """Test detection of longer cycles in references."""
        # Updated data to ensure B1 and C1 exist
        # We now have a 3x3 grid, ensuring A1, B1, C1 are valid references.
        # A1 -> B1
        # B1 -> C1
        # C1 -> A1
        data = [
            ["=B1", "=C1", "=A1"],
            ["", "", ""],
            ["", "", ""]
        ]
        sheet = Spreadsheet(data)
        with self.assertRaises(CircularReferenceError):
            sheet.evaluate()

    def test_invalid_reference_out_of_range(self):
        """Test handling of references that are out of the spreadsheet's range."""
        data = [
            ["=A2", "5"]
        ]
        sheet = Spreadsheet(data)
        with self.assertRaises(ValueError):
            sheet.evaluate()

    def test_invalid_token(self):
        """Test handling of invalid tokens in formulas."""
        data = [
            ["=A1+X"]  # 'X' is not a valid number or reference
        ]
        sheet = Spreadsheet(data)
        with self.assertRaises(ValueError):
            sheet.evaluate()

    def test_large_column_name(self):
        """Test references with large column names beyond 'Z'."""
        big_data = [
            ["1"] * 30  # 30 columns: A-Z, AA-AD
        ]
        # Add a second row with a valid formula referencing AA1 and AB1
        big_data.append([f"=AA1+AB1"] + [""] * 29)
        expected = [
            [1] * 30,
            [2] + [0] * 29  # AA1=1 (col26), AB1=1 (col27), A2=2
        ]
        sheet = Spreadsheet(big_data)
        result = sheet.evaluate()
        self.assertEqual(result, expected)

    def test_empty_cells_everywhere(self):
        """Test evaluation when all cells are empty."""
        data = [
            ["" for _ in range(5)]
            for _ in range(3)
        ]
        expected = [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]
        sheet = Spreadsheet(data)
        result = sheet.evaluate()
        self.assertEqual(result, expected)

    def test_mixed_complex_references(self):
        """Test mixed complex references and arithmetic operations."""
        data = [
            ["10", "=A1+5", "=B1-3"],
            ["=C1+2", "=A1+B1", "=B2-A2"],
            ["=C1+C2", "=A2+10", "=A1-C2"]
        ]
        expected = [
            [10, 15, 12],
            [14, 25, 11],
            [23, 24, -1]
        ]
        sheet = Spreadsheet(data)
        result = sheet.evaluate()
        self.assertEqual(result, expected)

    def test_negative_numbers(self):
        """Test handling of negative numbers in cells and formulas."""
        data = [
            ["-5", "10", "=A1+B1"],
            ["=B1-C1", "=A1-15", "=A2+B2"]
        ]
        expected = [
            [-5, 10, 5],
            [5, -20, -15]
        ]
        sheet = Spreadsheet(data)
        result = sheet.evaluate()
        self.assertEqual(result, expected)

    def test_whitespace_handling(self):
        """Test formulas with leading/trailing whitespaces."""
        data = [
            [" 5 ", " 10", " "],
            ["= A1 + 5", " =B1 -5 ", "= A1 + B1 "]
        ]
        expected = [
            [5, 10, 0],
            [10, 5, 15]
        ]
        sheet = Spreadsheet(data)
        result = sheet.evaluate()
        self.assertEqual(result, expected)

    def test_empty_spreadsheet(self):
        """Test behavior when the spreadsheet has no data."""
        data = []
        expected = []
        sheet = Spreadsheet(data)
        result = sheet.evaluate()
        self.assertEqual(result, expected)

    def test_utills_conversion(self):
        """Test the Utills.convert_26_base_to_decimal method."""
        test_cases = {
            "A": 1,
            "Z": 26,
            "AA": 27,
            "AB": 28,
            "BA": 53,
            "ZZ": 702,
            "AAA": 703,
            "aA": 27,  # Case-insensitive
            "zz": 702
        }
        for col_label, expected in test_cases.items():
            with self.subTest(col_label=col_label):
                result = Utills.convert_26_base_to_decimal(col_label)
                self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
