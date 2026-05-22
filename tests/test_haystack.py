"""Tests para construcción del heno."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from haystack import build_haystack, estimate_tokens


class TestBuildHaystack(unittest.TestCase):
    def test_returns_string(self):
        h = build_haystack(target_chars=1000)
        self.assertIsInstance(h, str)

    def test_at_least_target_chars(self):
        h = build_haystack(target_chars=5000)
        self.assertGreaterEqual(len(h), 5000)

    def test_diverse_content(self):
        """El heno debe usar al menos 3 párrafos base distintos para evitar
        artefactos de tokenización por repetición exacta."""
        h = build_haystack(target_chars=10000)
        # Debe contener trazas de los tres temas (ML, biología, historia)
        h_lower = h.lower()
        self.assertTrue("transformer" in h_lower or "atención" in h_lower)
        self.assertTrue("plantas" in h_lower or "fotosíntesis" in h_lower or "energía" in h_lower)
        self.assertTrue("renacimiento" in h_lower or "leonardo" in h_lower or "siglo" in h_lower)


class TestEstimateTokens(unittest.TestCase):
    def test_returns_positive(self):
        self.assertGreater(estimate_tokens("Hola mundo"), 0)

    def test_grows_with_length(self):
        short = estimate_tokens("Hola")
        long = estimate_tokens("Hola " * 100)
        self.assertGreater(long, short)


if __name__ == "__main__":
    unittest.main()
