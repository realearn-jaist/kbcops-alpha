import sys
import unittest
from unittest.mock import MagicMock, call, mock_open, patch

sys.path.append("../backend")
from models.extract_model import (
    load_annotations,
    load_axioms,
    load_classes,
    load_individuals,
    save_annotations,
    save_axioms,
    save_classes,
    save_individuals,
)


class TestOntologyModelOperations(unittest.TestCase):
    """Test cases for extract_model.py"""

    @patch("models.extract_model.getPath_ontology_directory")
    @patch("builtins.open", new_callable=mock_open)
    def test_save_axioms(self, mock_open, mock_getPath):
        """Test save_axioms function in extract_model.py

        Args:
            mock_open: MagicMock object
            mock_getPath: MagicMock object
        Returns:
            None
        """
        mock_getPath.return_value = "\\fake\\path"
        axioms = ["axiom1", "axiom2"]

        result = save_axioms("test_id", axioms)

        mock_open.assert_called_once_with(
            "\\fake\\path\\axioms.txt", "w", encoding="utf-8"
        )
        handle = mock_open()
        handle.write.assert_any_call("axiom1\n")
        handle.write.assert_any_call("axiom2\n")
        self.assertEqual(result, axioms)

    @patch("models.extract_model.getPath_ontology_directory")
    @patch("builtins.open", new_callable=mock_open)
    def test_save_classes(self, mock_open, mock_getPath):
        """Test save_classes function in extract_model.py

        Args:
            mock_open: MagicMock object
            mock_getPath: MagicMock object
        Returns:
            None
        """
        mock_getPath.return_value = "\\fake\\path"
        classes = {"class1", "class2"}

        result = save_classes("test_id", classes)

        mock_open.assert_called_once_with(
            "\\fake\\path\\classes.txt", "w", encoding="utf-8"
        )
        handle = mock_open()
        handle.write.assert_any_call("class1\n")
        handle.write.assert_any_call("class2\n")
        self.assertEqual(result, classes)

    @patch("models.extract_model.getPath_ontology_directory")
    @patch("builtins.open", new_callable=mock_open)
    def test_save_individuals(self, mock_open, mock_getPath):
        """Test save_individuals function in extract_model.py

        Args:
            mock_open: MagicMock object
            mock_getPath: MagicMock object
        Returns:
            None
        """
        mock_getPath.return_value = "\\fake\\path"
        individuals = {"ind1", "ind2"}

        result = save_individuals("test_id", individuals)

        mock_open.assert_called_once_with(
            "\\fake\\path\\individuals.txt", "w", encoding="utf-8"
        )
        handle = mock_open()
        handle.write.assert_any_call("ind1\n")
        handle.write.assert_any_call("ind2\n")
        self.assertEqual(result, individuals)

    @patch("models.extract_model.getPath_ontology_directory")
    @patch("builtins.open", new_callable=mock_open)
    def test_save_annotations(self, mock_open, mock_getPath):
        """Test save_annotations function in extract_model.py

        Args:
            mock_open: MagicMock object
            mock_getPath: MagicMock object
        Returns:
            None
        """
        mock_getPath.return_value = "\\fake\\path"
        annotations = [["ann1", "ann2"], ["ann3", "ann4"]]
        projection = MagicMock()
        projection.entityToPreferredLabels = {
            "e1": {"label1"},
            "e2": {"label2"},
        }

        result = save_annotations("test_id", annotations, projection)

        # mock_open.assert_any_call(
        #     "\\fake\\path\\annotations.txt", "w", encoding="utf-8"
        # )
        calls = [
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
        mock_open.assert_has_calls(calls)

    @patch("models.extract_model.getPath_ontology_directory")
    @patch("builtins.open", new_callable=mock_open, read_data="axiom1\naxiom2\n")
    def test_load_axioms(self, mock_open, mock_getPath):
        """Test load_axioms function in extract_model.py

        Args:
            mock_open: MagicMock object
            mock_getPath: MagicMock object
        Returns:
            None
        """
        mock_getPath.return_value = "\\fake\\path"

        result = load_axioms("test_id")

        mock_open.assert_called_once_with(
            "\\fake\\path\\axioms.txt", "r", encoding="utf-8"
        )
        self.assertEqual(result, ["axiom1", "axiom2"])

    @patch("models.extract_model.getPath_ontology_directory")
    @patch("builtins.open", new_callable=mock_open, read_data="class1\nclass2\n")
    def test_load_classes(self, mock_open, mock_getPath):
        """Test load_classes function in extract_model.py

        Args:
            mock_open: MagicMock object
            mock_getPath: MagicMock object
        Returns:
            None
        """
        mock_getPath.return_value = "\\fake\\path"

        result = load_classes("test_id")

        mock_open.assert_called_once_with(
            "\\fake\\path\\classes.txt", "r", encoding="utf-8"
        )
        self.assertEqual(result, ["class1", "class2"])

    @patch("models.extract_model.getPath_ontology_directory")
    @patch("builtins.open", new_callable=mock_open, read_data="ind1\nind2\n")
    def test_load_individuals(self, mock_open, mock_getPath):
        """Test load_individuals function in extract_model.py

        Args:
            mock_open: MagicMock object
            mock_getPath: MagicMock object
        Returns:
            None
        """
        mock_getPath.return_value = "\\fake\\path"

        result = load_individuals("test_id")

        mock_open.assert_called_once_with(
            "\\fake\\path\\individuals.txt", "r", encoding="utf-8"
        )
        self.assertEqual(result, ["ind1", "ind2"])

    @patch("models.extract_model.getPath_ontology_directory")
    def test_load_annotations(self, mock_getPath):
        """Test load_annotations function in extract_model.py

        Args:
            mock_getPath: MagicMock object
        Returns:
            None
        """

        # Mock the return value of getPath_ontology_directory
        mock_getPath.return_value = "\\fake\\path"

        # Mock data for the files
        annotation_data = "ann1 ann2\nann3 ann4 ann5\n"
        urilabel_data = "e1 label1\ne2 label2\n"

        # Patch the built-in open function with mock_open for annotations.txt
        with patch(
            "builtins.open", mock_open(read_data=annotation_data)
        ) as mock_open_annotation:
            # Call the function under test
            result_anno = load_annotations("test_id")

            # Assert the expected call for annotations.txt
            mock_open_annotation.assert_any_call(
                "\\fake\\path\\annotations.txt", "r", encoding="utf-8"
            )

        # Patch the built-in open function with mock_open for uri_labels.txt
        with patch(
            "builtins.open", mock_open(read_data=urilabel_data)
        ) as mock_open_urilabel:
            # Call the function under test again
            result_uri = load_annotations("test_id")

            # Assert the expected call for uri_labels.txt
            mock_open_urilabel.assert_any_call(
                "\\fake\\path\\uri_labels.txt", "r", encoding="utf-8"
            )

        result = (result_uri[0], result_anno[1])

        # Expected results
        expected_uri_label = ["e1 label1", "e2 label2"]
        expected_annotation = ["ann1 ann2", "ann3 ann4 ann5"]
        self.assertEqual(result, (expected_uri_label, expected_annotation))


if __name__ == "__main__":
    unittest.main()
