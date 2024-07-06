import os
import sys
import unittest
from unittest import mock
from unittest.mock import MagicMock, Mock, mock_open, patch
from owlready2 import World

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
        class_individual_list, truth_list, predict_list = gm.extract_garbage_value(
            mock_data
        )

        # Assert the expected results
        self.assertEqual(class_individual_list, ["Ind1", "Ind2"])
        self.assertEqual(truth_list, ["True1", "True2"])
        self.assertEqual(predict_list, ["Pred1", "Pred2"])

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

    @patch("controllers.graph_controller.World")
    @patch("controllers.graph_controller.nx.nx_pydot.graphviz_layout")
    @patch("controllers.graph_controller.nx.draw")
    @patch("controllers.graph_controller.replace_or_create_folder")
    @patch("controllers.graph_controller.find_parents_with_relations")
    @patch("controllers.graph_controller.plt.savefig")
    @patch("builtins.open", new_callable=mock_open)
    def test_graph_maker(
        self,
        mock_open,
        mock_savefig,
        mock_find_parents_with_relations,
        mock_replace_or_create_folder,
        mock_draw,
        mock_layout,
        mock_World,
    ):
        """Test graph_maker function in graph_controller.py

        Args:
            mock_open: MagicMock object
            mock_savefig: MagicMock object
            mock_find_parents_with_relations: MagicMock object
            mock_replace_or_create_folder: MagicMock object
            mock_draw: MagicMock object
            mock_layout: MagicMock object
            mock_World: MagicMock object
        Returns:
            None
        """
        mock_layout.return_value = {
            "Ind1": (0, 0),
            "True1": (1, 1),
            "Pred1": (3, 3),
            "owl.Thing": (4, 4),
        }
        mock_replace_or_create_folder.return_value = None
        mock_find_parents_with_relations.return_value = [
            ["Ind1", "relation", "True1"],
            ["True1", "relation", "Pred1"],
            ["Pred1", "relation", "owl.Thing"],
        ]
        fig_directory = "fig_directory"

        entity_prefix = "http://example.com#"
        class_individual_list = ["Ind1"]
        truth_list = ["True1"]
        predict_list = ["Pred1"]

        mock_world_instance = MagicMock()
        mock_World.return_value = mock_world_instance
        mock_ontology_instance = MagicMock()
        mock_world_instance.get_ontology.return_value = mock_ontology_instance
        mock_ontology_instance.load.return_value = mock_ontology_instance
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
                onto_type="tbox",
                onto_file=mock_ontology,
                entity_prefix=entity_prefix,
                entity_split=".",
                class_individual_list=class_individual_list,
                truth_list=truth_list,
                predict_list=predict_list,
                fig_directory=fig_directory,
            )
        mock_open.assert_called_with(os.path.join("fig_directory", "graph_0.dot"), "w")

    @patch("controllers.graph_controller.coverage_class")
    @patch("controllers.graph_controller.World")
    @patch("controllers.graph_controller.load_multi_input_files")
    @patch("controllers.graph_controller.get_prefix")
    @patch("controllers.graph_controller.graph_maker", return_value=None)
    @patch("controllers.graph_controller.read_garbage_metrics_pd")
    @patch("controllers.graph_controller.extract_garbage_value")
    @patch("controllers.graph_controller.load_graph")
    @patch("controllers.graph_controller.get_path")
    @patch("controllers.graph_controller.replace_or_create_folder")
    def test_create_graph(
        self,
        mock_replace_or_create_folder,
        mock_get_path,
        mock_load_graph,
        mock_extract_garbage_value,
        mock_read_garbage_metrics_pd,
        mock_graph_maker,
        mock_get_prefix,
        mock_load_multi_input_files,
        mock_world,
        mock_coverage_class,
    ):
        """Test create_graph function in graph_controller.py

        Args:
            mock_replace_or_create_folder: MagicMock object
            mock_get_path: MagicMock object
            mock_load_graph: MagicMock object
            mock_extract_garbage_value: MagicMock object
            mock_read_garbage_metrics_pd: MagicMock object
            mock_graph_maker: MagicMock object
            mock_get_prefix: MagicMock object
            mock_load_multi_input_files: MagicMock object
            mock_world: MagicMock object
            mock_coverage_class: MagicMock object
        Returns:
            None
        """

        ontology_name = "test_ontology"
        algorithm = "test_algo"
        classifier = "test_classifier"

        # Mock return values for the dependencies
        mock_load_multi_input_files.return_value = {
            "individuals": ["http://example.com#Ind1", "http://example.com#Ind2"],
            "classes": ["http://example.com#Class1", "http://example.com#Class2"],
        }

        mock_get_prefix.return_value = "http://example.com#"
        mock_coverage_class.return_value = 20

        # Mock ontology and graph data
        mock_ontology = Mock()
        mock_world.return_value.get_ontology.return_value.load.return_value = (
            mock_ontology
        )
        mock_ontology.search.return_value = ["mock_search_result"]

        mock_read_garbage_metrics_pd.return_value = "mock_garbage_metrics_data"
        mock_extract_garbage_value.return_value = (
            ["Ind1", "Ind2"],
            ["True1", "True2"],
            ["Pred1", "Pred2"],
        )
        mock_load_graph.return_value = "mock_graph_data"

        # Mock get_path to return the desired paths
        def mock_get_path_side_effect(*args):
            if len(args) == 4 and args[3] == "graph_fig":
                return "\\fake\\path\\test_algo\\test_classifier\\graph_fig"
            elif args[1] == "test_ontology.owl":
                return "\\fake\\path\\ontology.owl"
            else:
                return "\\fake\\path\\other"

        mock_get_path.side_effect = mock_get_path_side_effect

        # Call the function under test
        result = gm.create_graph(ontology_name, algorithm, classifier)

        # Assert the expected calls and results
        mock_get_path.assert_any_call(ontology_name, algorithm, classifier, "graph_fig")
        mock_replace_or_create_folder.assert_called_once_with(
            "\\fake\\path\\test_algo\\test_classifier\\graph_fig"
        )

        mock_load_multi_input_files.assert_called_once_with(
            ontology_name, ["individuals", "classes"]
        )
        mock_world.return_value.get_ontology.assert_called_once_with(
            "\\fake\\path\\ontology.owl"
        )
        mock_read_garbage_metrics_pd.assert_called_once_with(
            ontology_name, algorithm, classifier
        )
        mock_extract_garbage_value.assert_called_once_with("mock_garbage_metrics_data")
        mock_graph_maker.assert_called_once_with(
            "abox",
            mock_ontology,
            "http://example.com#",
            ".",
            ["Ind1", "Ind2"],
            ["True1", "True2"],
            ["Pred1", "Pred2"],
            "\\fake\\path\\test_algo\\test_classifier\\graph_fig",
        )
        mock_load_graph.assert_called_once_with(ontology_name, algorithm, classifier)
        self.assertEqual(result, "mock_graph_data")


if __name__ == "__main__":
    unittest.main()
