"""Tests para MockRunner (los runners reales requieren claves API)."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from needle import generate_needle, insert_needle, extract_key_from_needle
from runners.mock_runner import MockRunner


class TestMockRunner(unittest.TestCase):
    def setUp(self):
        self.runner = MockRunner()
        self.haystack = "lorem ipsum " * 200
        self.needle = generate_needle(seed=42)
        self.key = extract_key_from_needle(self.needle)

    def test_finds_needle_at_start(self):
        context = insert_needle(self.haystack, self.needle, pos_ratio=0.05)
        answer = self.runner.query(context, "¿Cuál es la clave?")
        self.assertEqual(answer, self.key)

    def test_finds_needle_at_end(self):
        context = insert_needle(self.haystack, self.needle, pos_ratio=0.95)
        answer = self.runner.query(context, "¿Cuál es la clave?")
        self.assertEqual(answer, self.key)

    def test_fails_in_the_middle(self):
        context = insert_needle(self.haystack, self.needle, pos_ratio=0.5)
        answer = self.runner.query(context, "¿Cuál es la clave?")
        self.assertNotEqual(answer, self.key)

    def test_returns_no_encontrada_when_no_key(self):
        plain = "lorem ipsum " * 200
        answer = self.runner.query(plain, "¿Cuál es la clave?")
        self.assertEqual(answer, "no encontrada")

    def test_runner_has_name_and_model(self):
        self.assertEqual(self.runner.name, "mock")
        self.assertTrue(self.runner.model)


class TestRunnerImports(unittest.TestCase):
    def test_mock_runner_always_importable(self):
        from runners import MockRunner
        self.assertIsNotNone(MockRunner)


if __name__ == "__main__":
    unittest.main()
