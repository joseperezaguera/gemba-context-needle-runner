"""Tests para el orquestador del experimento needle-in-haystack."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from curve import run_curve
from runners.mock_runner import MockRunner


class TestRunCurve(unittest.TestCase):
    def setUp(self):
        self.runner = MockRunner()

    def test_returns_recall_per_position(self):
        results = run_curve(
            runner=self.runner,
            haystack_chars=3000,
            positions=[0.05, 0.5, 0.95],
            n_trials=3,
            seed=42,
        )
        self.assertEqual(set(results.keys()), {0.05, 0.5, 0.95})

    def test_recall_in_unit_interval(self):
        results = run_curve(
            runner=self.runner,
            haystack_chars=3000,
            positions=[0.05, 0.5, 0.95],
            n_trials=5,
            seed=0,
        )
        for pos, recall in results.items():
            self.assertGreaterEqual(recall, 0.0, f"recall<0 en pos={pos}")
            self.assertLessEqual(recall, 1.0, f"recall>1 en pos={pos}")

    def test_mock_runner_recall_pattern(self):
        """MockRunner: alto en extremos, bajo en el medio."""
        results = run_curve(
            runner=self.runner,
            haystack_chars=3000,
            positions=[0.05, 0.5, 0.95],
            n_trials=5,
            seed=42,
        )
        self.assertGreaterEqual(results[0.05], results[0.5])
        self.assertGreaterEqual(results[0.95], results[0.5])

    def test_deterministic_with_seed(self):
        r1 = run_curve(self.runner, 3000, [0.05, 0.5, 0.95], n_trials=3, seed=42)
        r2 = run_curve(self.runner, 3000, [0.05, 0.5, 0.95], n_trials=3, seed=42)
        self.assertEqual(r1, r2)


if __name__ == "__main__":
    unittest.main()
