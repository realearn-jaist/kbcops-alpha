import sys
import unittest
from unittest.mock import MagicMock, patch
from models import embed_model as om

sys.path.append("../backend")


class TestModelFunctions(unittest.TestCase):
    """Test cases for embed_model.py"""

    @patch("models.embed_model.get_path")
    @patch("os.path.exists")
    def test_isModelExist(self, mock_exists, mock_get_path):
        """Test that isModelExist function in embed_model.py

        Args:
            mock_exists: MagicMock object
            mock_get_path: MagicMock object
        Returns:
            None
        """
        mock_get_path.return_value = "/fake/path"
        mock_exists.return_value = True
        self.assertTrue(om.isModelExist("ontology", "algorithm"))

        mock_exists.return_value = False
        self.assertFalse(om.isModelExist("ontology", "algorithm"))

    @patch("models.embed_model.replace_or_create_folder")
    @patch("models.embed_model.get_path")
    @patch("joblib.dump")
    @patch("gensim.models.word2vec.Word2Vec.save")
    def test_save_model(
        self, mock_gensim_save, mock_joblib_dump, mock_get_path, mock_replace_folder
    ):
        """Test save_model function in embed_model.py

        Args:
            mock_gensim_save: MagicMock object
            mock_joblib_dump: MagicMock object
            mock_get_path: MagicMock object
            mock_replace_folder: MagicMock object
        Returns:
            None
        """
        model = MagicMock()
        algorithm = "rdf2vec"

        mock_get_path.return_value = f"\\fake\\path\\{algorithm}"

        om.save_model("ontology", algorithm, model)
        mock_joblib_dump.assert_called_once_with(
            model, f"\\fake\\path\\{algorithm}\\model"
        )
        mock_replace_folder.assert_called_once_with(f"\\fake\\path\\{algorithm}")

        mock_joblib_dump.reset_mock()
        mock_replace_folder.reset_mock()

        algorithm = "word2vec"
        mock_get_path.return_value = f"\\fake\\path\\{algorithm}"

        om.save_model("ontology", algorithm, model)
        model.save.assert_called_once_with(f"\\fake\\path\\{algorithm}\\model")
        mock_replace_folder.assert_called_once_with(f"\\fake\\path\\{algorithm}")

    @patch("models.embed_model.get_path")
    @patch("joblib.load")
    @patch("gensim.models.word2vec.Word2Vec.load")
    @patch("os.path.exists")
    def test_load_model(
        self, mock_exists, mock_gensim_load, mock_joblib_load, mock_get_path
    ):
        """Test load_model function in embed_model.py

        Args:
            mock_exists: MagicMock object
            mock_gensim_load: MagicMock object
            mock_joblib_load: MagicMock object
            mock_get_path: MagicMock object
        Returns:
            None
        """
        algorithm = "rdf2vec"

        mock_get_path.return_value = f"\\fake\\path\\{algorithm}\\model"
        mock_exists.return_value = True

        # Call the function under test
        result = om.load_model("ontology", algorithm)

        # Assert that joblib.load was called with the correct path
        mock_joblib_load.assert_called_once_with(f"\\fake\\path\\{algorithm}\\model")
        self.assertIsNotNone(
            result
        )  # Assuming load_model returns None when model doesn't exist

        algorithm = "word2vec"

        mock_get_path.return_value = f"\\fake\\path\\{algorithm}\\model"
        mock_exists.return_value = True

        # Call the function under test
        result = om.load_model("ontology", algorithm)

        # Assert that gensim.models.word2vec.Word2Vec.load was called with the correct path
        mock_gensim_load.assert_called_once_with(f"\\fake\\path\\{algorithm}\\model")
        self.assertIsNotNone(
            result
        )  # Assuming load_model returns None when model doesn't exist

        mock_exists.return_value = False

        # Test when model doesn't exist
        result = om.load_model("ontology", "rdf2vec")
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
