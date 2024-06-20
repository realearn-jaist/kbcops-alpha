import os
import sys
import unittest
from unittest import mock
from unittest.mock import MagicMock, patch

# Assuming the module is named 'controllers.graph_controller'
sys.path.append("../backend")
import controllers.graph_controller as gm
import pandas as pd


class TestGraphModule(unittest.TestCase):
    """Test cases for graph_controller.py"""

    def test_extract_garbage_value(self):
        """Test extract_garbage_value function in graph_controller.py

        Args:
            self: TestGraphModule object
        Returns:
            None
        """
        # Create a mock DataFrame
        mock_data = pd.DataFrame(
            {
                "Individual": ["Ind1", "Ind2"],
                "True": ["True1", "True2"],
                "Predicted": ["Pred1", "Pred2"],
            }
        )

        # Call the function under test
        individuals, truths, predictions = gm.extract_garbage_value(mock_data)

        # Assert the expected results
        self.assertEqual(individuals, ["Ind1", "Ind2"])
        self.assertEqual(truths, ["True1", "True2"])
        self.assertEqual(predictions, ["Pred1", "Pred2"])

    def test_get_prefix(self):
        """Test get_prefix function in graph_controller.py
        Args:
            self: TestGraphModule object
        Returns:
            None
        """
        value_with_hash = "http://example.com#Entity"
        value_with_slash = "http://example.com/Entity"

        self.assertEqual(gm.get_prefix(value_with_hash), "http://example.com#")
        self.assertEqual(gm.get_prefix(value_with_slash), "http://example.com/")

    @patch("controllers.graph_controller.nx.nx_pydot.graphviz_layout")
    @patch("controllers.graph_controller.nx.draw")
    @patch("controllers.graph_controller.replace_or_create_folder")
    @patch("controllers.graph_controller.plt.savefig")
    def test_graph_maker(
        self, mock_savefig, mock_replace_or_create_folder, mock_draw, mock_layout
    ):
        """Test graph_maker function in graph_controller.py

        Args:
            mock_savefig: MagicMock object
            mock_replace_or_create_folder: MagicMock object
            mock_draw: MagicMock object
            mock_layout: MagicMock object
        Returns:
            None
        """
        mock_layout.return_value = {"Entity1": (0, 0), "Entity2": (1, 1)}
        mock_replace_or_create_folder.return_value = None

        entity_prefix = "http://example.com#"
        individual_list = ["Entity1", "Entity2"]
        truth_list = ["True1", "True2"]
        predict_list = ["Pred1", "Pred2"]
        fig_directory = "fake_directory"

        mock_ontology = MagicMock()
        mock_ontology.search.return_value = [MagicMock()]

        # Mock the search results for the ontology
        def mock_search(iri):
            entity = MagicMock()
            entity.INDIRECT_is_a = ["owl.Thing"]
            return [entity]

        mock_ontology.search.side_effect = mock_search

        with patch(
            "controllers.graph_controller.get_ontology", return_value=mock_ontology
        ):
            gm.graph_maker(
                "TBox",
                mock_ontology,
                entity_prefix,
                individual_list,
                truth_list,
                predict_list,
                fig_directory,
            )

        self.assertTrue(mock_savefig.called)
        self.assertTrue(mock_draw.called)
        self.assertTrue(mock_layout.called)

    @patch("controllers.graph_controller.get_ontology")
    @patch("controllers.graph_controller.load_individuals")
    @patch("controllers.graph_controller.load_classes")
    @patch("controllers.graph_controller.get_prefix")
    @patch("controllers.graph_controller.graph_maker")
    @patch("controllers.graph_controller.read_garbage_metrics_pd")
    @patch("controllers.graph_controller.extract_garbage_value")
    @patch("controllers.graph_controller.load_graph")
    @patch("controllers.graph_controller.getPath_ontology")
    @patch("controllers.graph_controller.getPath_ontology_directory")
    @patch("controllers.graph_controller.replace_or_create_folder")
    def test_create_graph(
        self,
        mock_replace_or_create_folder,
        mock_getPath_ontology_directory,
        mock_getPath_ontology,
        mock_load_graph,
        mock_extract_garbage_value,
        mock_read_garbage_metrics_pd,
        mock_graph_maker,
        mock_get_prefix,
        mock_load_classes,
        mock_load_individuals,
        mock_get_ontology,
    ):
        """Test create_graph function in graph_controller.py

        Args:
            self: TestGraphModule object
            mock_replace_or_create_folder: MagicMock object
            mock_getPath_ontology_directory: MagicMock object
            mock_getPath_ontology: MagicMock object
            mock_load_graph: MagicMock object
            mock_extract_garbage_value: MagicMock object
            mock_read_garbage_metrics_pd: MagicMock object
            mock_graph_maker: MagicMock object
            mock_get_prefix: MagicMock object
            mock_load_classes: MagicMock object
            mock_load_individuals: MagicMock object
            mock_get_ontology: MagicMock object
        Returns:
            None
        """

        id = "test_id"
        algo = "test_algo"

        # Mock return values for the dependencies
        mock_load_individuals.return_value = ["Ind1", "Ind2"]
        mock_load_classes.return_value = ["Class1", "Class2"]
        mock_get_prefix.return_value = "http://example.com#"
        mock_getPath_ontology_directory.return_value = "\\fake\\path"
        mock_getPath_ontology.return_value = "\\fake\\path\\ontology.owl"

        # Mock ontology and graph data
        mock_ontology = mock.Mock()
        mock_ontology.load.return_value = "mock_ontology_data"
        mock_get_ontology.return_value = mock_ontology

        mock_read_garbage_metrics_pd.return_value = "mock_garbage_metrics_data"
        mock_extract_garbage_value.return_value = (
            ["Ind1", "Ind2"],  # Mocking the extracted values
            ["True1", "True2"],
            ["Pred1", "Pred2"],
        )
        mock_load_graph.return_value = "mock_graph_data"

        # Call the function under test
        result = gm.create_graph(id, algo)

        # Assert the expected calls and results
        mock_getPath_ontology_directory.assert_called_once_with(id)
        mock_replace_or_create_folder.assert_called_once_with(
            "\\fake\\path\\test_algo\\graph_fig"
        )
        mock_load_individuals.assert_called_once_with(id)
        mock_load_classes.assert_called_once_with(id)
        mock_getPath_ontology.assert_called_once_with(id)
        mock_get_ontology.assert_called_once_with("\\fake\\path\\ontology.owl")
        mock_read_garbage_metrics_pd.assert_called_once_with(id, algo)
        mock_extract_garbage_value.assert_called_once_with("mock_garbage_metrics_data")
        mock_graph_maker.assert_called_once_with(
            "ABox",
            "mock_ontology_data",  # Ensure the ontology data matches
            "http://example.com#",
            ["Ind1", "Ind2"],
            ["True1", "True2"],
            ["Pred1", "Pred2"],
            "\\fake\\path\\test_algo\\graph_fig",
        )
        mock_load_graph.assert_called_once_with(id, algo)

        self.assertEqual(result, "mock_graph_data")


if __name__ == "__main__":
    unittest.main()
