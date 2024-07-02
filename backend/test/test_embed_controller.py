import sys
import unittest
from configparser import ConfigParser
from unittest.mock import MagicMock, patch

sys.path.append("../backend")
from main import create_app
from controllers.embed_controller import opa2vec_or_onto2vec, owl2vec_star, rdf2vec


class TestEmbedFunctions(unittest.TestCase):
    """Test cases for embed_controller.py"""

    @classmethod
    def setUp(self):
        """Create the Flask app and a test client for the app. Establish an application context before each test.

        Args:
            self: TestEmbedFunctions object
        Returns:
            None
        """
        self.app = create_app()
        self.app.testing = True
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    @patch(
        "controllers.embed_controller.load_multi_input_files",
        return_value={
            "axioms" : ["axiom1", "axiom2"], 
            "classes" : ["class1", "class2"], 
            "individuals" : ["individual1", "individual2"], 
            "uri_labels" : ["uri1 label1", "uri2 label2 label3"], 
            "annotations" : ["uri1 annotation1", "uri2 annotation2"]
        },
    )
    @patch("controllers.embed_controller.save_model", return_value=None)
    @patch("controllers.embed_controller.gensim.models.Word2Vec")
    def test_opa2vec_or_onto2vec(
        self,
        mock_Word2Vec,
        mock_save_model,
        mock_load_multi_input_files
    ):
        """Test opa2vec_or_onto2vec function in embed_controller.py

        Args:
            self: TestEmbedFunctions object
            mock_Word2Vec: MagicMock object
            mock_save_model: MagicMock object
            mock_load_annotations: MagicMock object
            mock_load_individuals: MagicMock object
            mock_load_classes: MagicMock object
            mock_load_axioms: MagicMock object
        Returns:
            None
        """

        mock_config_parser = MagicMock(ConfigParser)
        mock_config_parser.return_value.read_file = MagicMock(return_value=None)
        with patch(
            "controllers.embed_controller.configparser.ConfigParser",
            return_value=mock_config_parser,
        ):
            result = opa2vec_or_onto2vec("ontology_name", "config_file", "opa2vec")

            self.assertEqual(result, "opa2vec embedded success!!")
            mock_load_multi_input_files.assert_called_once_with("ontology_name", ["axioms", "classes", "individuals", "uri_labels", "annotations"])
            mock_Word2Vec.assert_called_once()

    @patch(
        "controllers.embed_controller.load_multi_input_files",
        return_value={
            "axioms" : ["axiom1", "axiom2"], 
            "classes" : ["class1", "class2"], 
            "individuals" : ["individual1", "individual2"], 
            "uri_labels" : ["uri1 label1", "uri2 label2 label3"], 
            "annotations" : ["uri1 annotation1", "uri2 annotation2"]
        },
    )
    @patch("controllers.embed_controller.save_model", return_value=None)
    @patch("controllers.embed_controller.gensim.models.Word2Vec")
    def test_owl2vec_star(
        self,
        mock_Word2Vec,
        mock_save_model,
        mock_load_multi_input_files,
    ):
        """Test owl2vec_star function in embed_controller.py

        Args:
            self: TestEmbedFunctions object
            mock_Word2Vec: MagicMock object
            mock_save_model: MagicMock object
            mock_load_annotations: MagicMock object
            mock_load_individuals: MagicMock object
            mock_load_classes: MagicMock object
            mock_load_axioms: MagicMock object
        Returns:
            None
        """

        mock_config_parser = MagicMock(ConfigParser)
        mock_config_parser.return_value.read_file = MagicMock(return_value=None)
        with patch(
            "controllers.embed_controller.configparser.ConfigParser",
            return_value=mock_config_parser,
        ):
            result = owl2vec_star("ontology_name", "config_file", "owl2vec-star")

            self.assertEqual(result, "owl2vec-star embedded success!!")
            mock_load_multi_input_files.assert_called_once_with("ontology_name", ["axioms", "classes", "individuals", "uri_labels", "annotations"])
            mock_Word2Vec.assert_called_once()

    @patch(
        "controllers.embed_controller.load_multi_input_files",
        return_value={ 
            "classes" : ["class1", "class2"], 
            "individuals" : ["individual1", "individual2"],
        },
    )
    @patch("controllers.embed_controller.save_model", return_value=None)
    @patch(
        "controllers.embed_controller.get_rdf2vec_embed",
        return_value=(None, "mock_model"),
    )
    def test_rdf2vec(
        self,
        mock_get_rdf2vec_embed,
        mock_save_model,
        mock_load_multi_input_files,
    ):
        """Test rdf2vec function in embed_controller.py

        Args:
            self: TestEmbedFunctions object
            mock_get_rdf2vec_embed: MagicMock object
            mock_save_model: MagicMock object
            mock_load_annotations: MagicMock object
            mock_load_individuals: MagicMock object
            mock_load_classes: MagicMock object
            mock_load_axioms: MagicMock object
        Returns:
            None
        """
        mock_config_parser = MagicMock(ConfigParser)
        mock_config_parser.return_value.read_file = MagicMock(return_value=None)
        with patch(
            "controllers.embed_controller.configparser.ConfigParser",
            return_value=mock_config_parser,
        ):
            result = rdf2vec("ontology_name", "config_file", "rdf2vec")

            self.assertEqual(result, "rdf2vec embedded success!!")
            mock_load_multi_input_files.assert_called_once_with("ontology_name", ["classes", "individuals"])
            mock_get_rdf2vec_embed.assert_called_once()


if __name__ == "__main__":
    unittest.main()
