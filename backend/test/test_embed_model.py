import sys
import unittest
from unittest.mock import MagicMock, patch
from models import embed_model as om

sys.path.append("../backend")


class TestModelFunctions(unittest.TestCase):

    @patch("models.embed_model.getPath_ontology_directory")
    @patch("os.path.exists")
    def test_isModelExist(self, mock_exists, mock_getPath):
        """Test that isModelExist function in embed_model.py"""
        mock_getPath.return_value = "/fake/path"
        mock_exists.return_value = True
        self.assertTrue(om.isModelExist("ontology", "algorithm"))

        mock_exists.return_value = False
        self.assertFalse(om.isModelExist("ontology", "algorithm"))

    @patch("utils.file_handler.replace_or_create_folder")
    @patch("models.embed_model.getPath_ontology_directory")
    @patch("joblib.dump")
    @patch("gensim.models.word2vec.Word2Vec.save")
    def test_save_model(
        self, mock_gensim_save, mock_joblib_dump, mock_getPath, mock_replace_folder
    ):
        """Test save_model function in embed_model.py"""
        mock_getPath.return_value = "/fake/path"

        model = MagicMock()
        algorithm = "rdf2vec"
        om.save_model("ontology", algorithm, model)
        mock_joblib_dump.assert_called_once_with(
            model, f"/fake/path\\{algorithm}\\model"
        )

        algorithm = "word2vec"
        om.save_model("ontology", algorithm, model)
        model.save.assert_called_once_with(f"/fake/path\\{algorithm}\\model")

    @patch("models.embed_model.getPath_ontology_directory")
    @patch("joblib.load")
    @patch("gensim.models.word2vec.Word2Vec.load")
    @patch("os.path.exists")
    def test_load_model(
        self, mock_exists, mock_gensim_load, mock_joblib_load, mock_getPath
    ):
        """Test load_model function in embed_model.py"""
        mock_getPath.return_value = "/fake/path"
        mock_exists.return_value = True

        algorithm = "rdf2vec"
        om.load_model("ontology", algorithm)
        mock_joblib_load.assert_called_once_with(f"/fake/path\\{algorithm}\\model")

        algorithm = "word2vec"
        om.load_model("ontology", algorithm)
        mock_gensim_load.assert_called_once_with(f"/fake/path\\{algorithm}\\model")

        mock_exists.return_value = False
        self.assertIsNone(om.load_model("ontology", "rdf2vec"))


if __name__ == "__main__":
    unittest.main()
