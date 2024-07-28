import os
import sys
import unittest
from unittest.mock import MagicMock, patch

sys.path.append("../backend")
from main import create_app
from models.ontology_model import (
    list_ontology,
    save_ontology,
)


class TestOntologyModel(unittest.TestCase):
    @classmethod
    def setUp(self):
        """Create the Flask app and a test client for the app. Establish an application context before each test.

        Args:
            self: TestOntologyModel object
        Returns:
            None
        """
        self.app = create_app()
        self.app.testing = True

        self.client = self.app.test_client()

        self.app_context = self.app.app_context()
        self.app_context.push()

    @patch("models.ontology_model.current_app")
    @patch("models.ontology_model.replace_or_create_folder")
    def test_save_ontology(
        self, mock_replace_or_create_folder, mock_current_app
    ):
        """Test save_ontology function in ontology_model.py

        Args:
            mock_replace_or_create_folder: MagicMock object
            mock_current_app: MagicMock object
        Returns:
            None
        """
        app = create_app()
        app.config["STORAGE_FOLDER"] = "\\fake\\storage"
        mock_current_app.config = app.config

        file = MagicMock()
        id = "test_id"
        filename = "test_filename.owl"

        save_ontology(file, id, filename)

        expected_path = os.path.join("\\fake\\storage", id)
        mock_replace_or_create_folder.assert_called_once_with(expected_path)

    @patch("models.ontology_model.current_app")
    @patch("os.listdir")
    @patch("os.path.isdir")
    def test_list_ontology(self, mock_isdir, mock_listdir, mock_current_app):
        """Test list_ontology function in ontology_model.py

        Args:
            mock_isdir: MagicMock object
            mock_listdir: MagicMock object
            mock_current_app: MagicMock object
        Returns:
            None
        """
        app = create_app()
        app.config["STORAGE_FOLDER"] = "\\fake\\storage"
        mock_current_app.config = app.config
        mock_isdir.return_value = True
        mock_listdir.return_value = ["ontology1", "ontology2"]

        result = list_ontology()
        expected_path = "\\fake\\storage"

        mock_listdir.assert_called_once_with(expected_path)
        self.assertEqual(result, ["ontology1", "ontology2"])


if __name__ == "__main__":
    unittest.main()
