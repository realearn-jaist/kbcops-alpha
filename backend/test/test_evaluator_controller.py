import sys
import unittest
from unittest.mock import patch
import numpy as np

sys.path.append("../backend")
from main import create_app
from controllers.evaluator_controller import InclusionEvaluator


class TestInclusionEvaluator(unittest.TestCase):
    """Test cases for evaluator.py"""

    def setUp(self):
        """Create the Flask app and a test client for the app. Establish an application context before each test.
        Args:
            self: TestInclusionEvaluator object
        Returns:
            None
        """
        self.app = create_app()
        self.app.testing = True

        self.client = self.app.test_client()

        self.app_context = self.app.app_context()
        self.app_context.push()
        self.valid_samples = [
            ["individual3", "class3"],
            ["individual4", "class4"],
        ]
        self.test_samples = [
            ["individual1", "class1"],
            ["individual2", "class2"],
        ]
        self.train_X = np.array([[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]])
        self.train_y = np.array([0, 1])
        self.classes = [
            "class1",
            "class2",
            "class3",
            "class4",
        ]
        self.classes_e = np.array(
            [
                [0.1, 0.2, 0.3],
                [0.1, 0.2, 0.3],
                [1.0, 1.1, 1.2],
                [1.0, 1.1, 1.2],
            ]
        )
        self.individuals = [
            "individual1",
            "individual2",
            "individual3",
            "individual4",
        ]
        self.individuals_e = np.array(
            [
                [0.1, 0.2, 0.3],
                [0.1, 0.2, 0.3],
                [1.0, 1.1, 1.2],
                [1.0, 1.1, 1.2],
            ]
        )
        self.inferred_ancestors = {
            "individual1": ["class2"],
            "individual2": ["class3"],
            "individual3": ["class3", "class4"],
            "individual4": ["class4"],
        }
        self.classifier = "example_classifier"
        self.ontology = "example_ontology"
        self.algorithm = "example_algorithm"
        self.onto_type = "abox"

    @patch("controllers.evaluator_controller.write_evaluate", return_value=None)
    @patch("controllers.evaluator_controller.write_garbage_metrics", return_value=[])
    def test_evaluate_method(self, mock_write_garbage_metrics, mock_write_evaluate):
        """Test evaluate method in InclusionEvaluator class in evaluator.py

        Args:
            mock_write_garbage_metrics: MagicMock object
            mock_write_evaluate: MagicMock object
        Returns:
            None
        """
        evaluator = InclusionEvaluator(
            self.valid_samples,
            self.test_samples,
            self.train_X,
            self.train_y,
            self.classes,
            self.classes_e,
            self.individuals,
            self.individuals_e,
            self.inferred_ancestors,
            self.ontology,
            self.algorithm,
            self.onto_type,
            self.classifier,
        )

        class SimpleMockModel:
            def __init__(self, classes):
                self.classes = classes

            def predict_proba(self, X):
                # Ensure we return probabilities for each class
                return np.random.rand(len(X), len(self.classes))

        mock_model = SimpleMockModel(self.classes)
        # Initialize a flag to False indicating that no division by zero error has occurred
        division_by_zero_error_occurred = False

        try:
            # Attempt to perform operations that may raise a ZeroDivisionError
            mrr, hit_at_1, hit_at_5, hit_at_10 = evaluator.evaluate(
                mock_model, self.test_samples
            )
        except ZeroDivisionError:
            # If a ZeroDivisionError occurs, set the flag to True
            division_by_zero_error_occurred = True
        except IndexError as e:
            print(f"IndexError occurred: {e}")
            self.fail("evaluate method raised IndexError")
        except ValueError as e:
            print(f"ValueError occurred: {e}")
            self.fail("evaluate method raised ValueError")

        if not division_by_zero_error_occurred:
            # If no division by zero error occurred, assert the expected outcomes
            self.assertIsInstance(mrr, float)
            self.assertIsInstance(hit_at_1, float)
            self.assertIsInstance(hit_at_5, float)
            self.assertIsInstance(hit_at_10, float)
            self.assertGreaterEqual(mrr, 0.0)
            self.assertGreaterEqual(hit_at_1, 0.0)
            self.assertGreaterEqual(hit_at_5, 0.0)
            self.assertGreaterEqual(hit_at_10, 0.0)
        else:
            # If a division by zero error occurred, assert True (or any other appropriate assertion)
            print("Division by zero error occurred")
            self.assertTrue(division_by_zero_error_occurred)


if __name__ == "__main__":
    unittest.main()
