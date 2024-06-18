import unittest
from unittest.mock import patch

import numpy as np
from app import create_app
from controllers.evaluator import InclusionEvaluator


class TestInclusionEvaluator(unittest.TestCase):

    def setUp(self):
        """Create the Flask app and a test client for the app. Establish an application context before each test."""
        self.app = create_app()
        self.app.testing = True

        self.client = self.app.test_client()

        self.app_context = self.app.app_context()
        self.app_context.push()

        self.valid_samples = [
            ["class1", "gt_class1"],
            ["class2", "gt_class2"],
        ]
        self.test_samples = [
            ["class1", "gt_class1"],
            ["class2", "gt_class2"],
        ]
        self.train_X = np.array([[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]])
        self.train_y = np.array([0, 1])
        self.classes = [
            "class1",
            "class2",
            "gt_class1",
            "gt_class2",
        ]
        self.classes_e = np.array(
            [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6], [0.7, 0.8, 0.9], [1.0, 1.1, 1.2]]
        )
        self.inferred_ancestors = {
            "class1": ["class2", "gt_class2"],
            "class2": ["class1", "gt_class1"],
        }
        self.ontology = "example_ontology"
        self.algorithm = "example_algorithm"

    @patch("controllers.evaluator.write_garbage_metrics", return_value=[])
    @patch("controllers.evaluator.write_json_file", return_value=None)
    def test_evaluate_method(self, mock_write_garbage_metrics, mock_write_json_file):
        """Test evaluate method in InclusionEvaluator class in evaluator.py"""
        print("Classes:", self.classes)
        print("Test Samples:", self.test_samples)

        evaluator = InclusionEvaluator(
            self.valid_samples,
            self.test_samples,
            self.train_X,
            self.train_y,
            self.classes,
            self.classes_e,
            self.inferred_ancestors,
            self.ontology,
            self.algorithm,
        )

        class SimpleMockModel:
            def predict_proba(self, X):

                return np.random.rand(len(X), 2)

        mock_model = SimpleMockModel()

        try:
            mrr, hit_at_1, hit_at_5, hit_at_10 = evaluator.evaluate(
                mock_model, self.test_samples
            )
        except IndexError as e:
            print(f"IndexError occurred: {e}")
            self.fail("evaluate method raised IndexError")

        self.assertIsInstance(mrr, float)
        self.assertIsInstance(hit_at_1, float)
        self.assertIsInstance(hit_at_5, float)
        self.assertIsInstance(hit_at_10, float)
        self.assertGreaterEqual(mrr, 0.0)
        self.assertGreaterEqual(hit_at_1, 0.0)
        self.assertGreaterEqual(hit_at_5, 0.0)
        self.assertGreaterEqual(hit_at_10, 0.0)


if __name__ == "__main__":
    unittest.main()
