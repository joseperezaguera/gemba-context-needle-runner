"""Tests para generación e inserción de agujas."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from needle import generate_needle, extract_key_from_needle, insert_needle


class TestGenerateNeedle(unittest.TestCase):
    def test_deterministic_with_seed(self):
        n1 = generate_needle(seed=42)
        n2 = generate_needle(seed=42)
        self.assertEqual(n1, n2)

    def test_different_seeds_give_different_needles(self):
        n1 = generate_needle(seed=1)
        n2 = generate_needle(seed=2)
        self.assertNotEqual(n1, n2)

    def test_contains_six_alphanumeric_key(self):
        n = generate_needle(seed=0)
        key = extract_key_from_needle(n)
        self.assertEqual(len(key), 6)
        self.assertTrue(key.isalnum())
        self.assertTrue(key.isupper() or key.isdigit() or any(c.isupper() for c in key))


class TestExtractKey(unittest.TestCase):
    def test_extract_known_key(self):
        text = "El código secreto es ABC123 y nada más."
        self.assertEqual(extract_key_from_needle(text), "ABC123")

    def test_raises_when_no_key(self):
        with self.assertRaises(ValueError):
            extract_key_from_needle("Aquí no hay clave alfanumérica de seis chars.")


class TestInsertNeedle(unittest.TestCase):
    def test_insert_at_start(self):
        h = "x" * 100
        n = "AGUJA"
        out = insert_needle(h, n, pos_ratio=0.0)
        self.assertTrue(out.startswith("AGUJA"))

    def test_insert_at_end(self):
        h = "x" * 100
        n = "AGUJA"
        out = insert_needle(h, n, pos_ratio=1.0)
        self.assertTrue(out.endswith("AGUJA"))

    def test_insert_at_middle(self):
        h = "x" * 1000
        n = "AGUJA"
        out = insert_needle(h, n, pos_ratio=0.5)
        self.assertEqual(out.count("AGUJA"), 1)
        self.assertTrue(400 <= out.find("AGUJA") <= 600)

    def test_invalid_pos_raises(self):
        with self.assertRaises(ValueError):
            insert_needle("x" * 10, "n", pos_ratio=1.5)
        with self.assertRaises(ValueError):
            insert_needle("x" * 10, "n", pos_ratio=-0.1)


if __name__ == "__main__":
    unittest.main()
