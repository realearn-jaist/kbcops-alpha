import sys
import unittest
from unittest.mock import MagicMock, call, mock_open, patch

sys.path.append("../backend")
from models.extract_model import (
    save_annotations,
    save_axioms,
    save_classes,
    save_individuals,
)


class TestOntologyModelOperations(unittest.TestCase):
    """Test cases for extract_model.py"""

    @patch("models.extract_model.get_path")
    @patch("builtins.open", new_callable=mock_open)
    def test_save_axioms(self, mock_open, mock_get_path):
        """Test save_axioms function in extract_model.py

        Args:
            mock_open: MagicMock object
            mock_get_path: MagicMock object
        Returns:
            None
        """
        mock_get_path.return_value = "\\fake\\path\\axioms.txt"
        axioms = ["axiom1", "axiom2"]

        result = save_axioms("test_id", axioms)

        mock_open.assert_called_once_with(
            "\\fake\\path\\axioms.txt", "w", encoding="utf-8"
        )
        handle = mock_open()
        handle.write.assert_any_call("axiom1\n")
        handle.write.assert_any_call("axiom2\n")
        self.assertEqual(result, axioms)

    @patch("models.extract_model.get_path")
    @patch("builtins.open", new_callable=mock_open)
    def test_save_classes(self, mock_open, mock_get_path):
        """Test save_classes function in extract_model.py

        Args:
            mock_open: MagicMock object
            mock_get_path: MagicMock object
        Returns:
            None
        """
        mock_get_path.return_value = "\\fake\\path\\classes.txt"
        classes = {"class1", "class2"}

        result = save_classes("test_id", classes)

        mock_open.assert_called_once_with(
            "\\fake\\path\\classes.txt", "w", encoding="utf-8"
        )
        handle = mock_open()
        handle.write.assert_any_call("class1\n")
        handle.write.assert_any_call("class2\n")
        self.assertEqual(result, classes)

    @patch("models.extract_model.get_path")
    @patch("builtins.open", new_callable=mock_open)
    def test_save_individuals(self, mock_open, mock_get_path):
        """Test save_individuals function in extract_model.py

        Args:
            mock_open: MagicMock object
            mock_get_path: MagicMock object
        Returns:
            None
        """
        mock_get_path.return_value = "\\fake\\path\\individuals.txt"
        individuals = {"ind1", "ind2"}

        result = save_individuals("test_id", individuals)

        mock_open.assert_called_once_with(
            "\\fake\\path\\individuals.txt", "w", encoding="utf-8"
        )
        handle = mock_open()
        handle.write.assert_any_call("ind1\n")
        handle.write.assert_any_call("ind2\n")
        self.assertEqual(result, individuals)

    @patch("models.extract_model.get_path")
    @patch("builtins.open", new_callable=mock_open)
    def test_save_annotations(self, mock_open, mock_get_path):
        """Test save_annotations function in extract_model.py

        Args:
            mock_open: MagicMock object
            mock_get_path: MagicMock object
        Returns:
            None
        """
        mock_get_path.side_effect = [
            "\\fake\\path\\uri_labels.txt",
            "\\fake\\path\\annotations.txt",
            "\\fake\\path\\uri_labels.txt",
            "\\fake\\path\\annotations.txt",
        ]

        annotations = [["ann1", "ann2"], ["ann3", "ann4"]]
        projection = MagicMock()
        projection.entityToPreferredLabels = {
            "e1": {"label1"},
            "e2": {"label2"},
        }

        mock_open().readlines.side_effect = [
            ["e1 label1\n", "e2 label2\n"],
            ["ann1 ann2\n", "ann3 ann4\n"],
        ]

        result = save_annotations("test_id", annotations, projection)

        expected_result = [
            "e1 label1\n",
            "e2 label2\n",
            "ann1 ann2\n",
            "ann3 ann4\n",
        ]

        self.assertEqual(result, expected_result)

        # Assert that open was called correctly
        calls = [
            call("\\fake\\path\\uri_labels.txt", "w", encoding="utf-8"),
            call().__enter__(),
            call().write("e1 label1\n"),
            call().write("e2 label2\n"),
            call().__exit__(None, None, None),
            call("\\fake\\path\\uri_labels.txt", "r", encoding="utf-8"),
            call().__enter__(),
            call().readlines(),
            call().__exit__(None, None, None),
            call("\\fake\\path\\annotations.txt", "w", encoding="utf-8"),
            call().__enter__(),
            call().write("ann1 ann2\n"),
            call().write("ann3 ann4\n"),
            call().__exit__(None, None, None),
            call("\\fake\\path\\annotations.txt", "r", encoding="utf-8"),
            call().__enter__(),
            call().readlines(),
            call().__exit__(None, None, None),
        ]
        mock_open.assert_has_calls(calls, any_order=False)


if __name__ == "__main__":
    unittest.main()
