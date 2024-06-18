import os
import unittest
from unittest.mock import MagicMock, patch

# Assuming the module is named 'controllers.graph_controller'
import controllers.graph_controller as gm
import pandas as pd


class TestGraphModule(unittest.TestCase):

    @patch("controllers.graph_controller.get_ontology")
    @patch("controllers.graph_controller.pd.read_csv")
    def test_load_file(self, mock_read_csv, mock_get_ontology):
        """Test load_file function in graph_controller.py"""
        mock_csv = pd.DataFrame(
            {
                "Individual": ["Ind1", "Ind2"],
                "True": ["True1", "True2"],
                "Predicted": ["Pred1", "Pred2"],
            }
        )
        mock_read_csv.return_value = mock_csv

        mock_ontology = MagicMock()
        mock_get_ontology.return_value.load.return_value = mock_ontology

        id = "test_id"
        onto_file, garbage_file = gm.load_file(id)

        mock_read_csv.assert_called_once_with(
            os.path.abspath(f"backend\\storage\\{id}\\{id}_garbage.csv")
        )
        mock_get_ontology.assert_called_once_with(
            os.path.abspath(f"backend\\storage\\{id}\\{id}.owl")
        )
        self.assertEqual(garbage_file.shape, mock_csv.shape)
        self.assertEqual(onto_file, mock_ontology)

    def test_extract_garbage_value(self):
        """Test extract_grabage_value function in graph_controller.py"""
        mock_data = pd.DataFrame(
            {
                "Individual": ["Ind1", "Ind2"],
                "True": ["True1", "True2"],
                "Predicted": ["Pred1", "Pred2"],
            }
        )

        individuals, truths, predictions = gm.extract_grabage_value(mock_data)

        self.assertEqual(individuals, ["Ind1", "Ind2"])
        self.assertEqual(truths, ["True1", "True2"])
        self.assertEqual(predictions, ["Pred1", "Pred2"])

    def test_get_prefix(self):
        """Test get_prefix function in graph_controller.py"""
        value_with_hash = "http://example.com#Entity"
        value_with_slash = "http://example.com/Entity"

        self.assertEqual(gm.get_prefix(value_with_hash), "http://example.com#")
        self.assertEqual(gm.get_prefix(value_with_slash), "http://example.com/")

    @patch("controllers.graph_controller.nx.nx_pydot.graphviz_layout")
    @patch("controllers.graph_controller.nx.draw")
    @patch("controllers.graph_controller.plt.savefig")
    def test_graph_maker(self, mock_savefig, mock_draw, mock_layout):
        """Test graph_maker function in graph_controller.py"""
        mock_layout.return_value = {"Entity1": (0, 0), "Entity2": (1, 1)}

        entity_prefix = "http://example.com#"
        individual_list = ["Entity1", "Entity2"]
        truth_list = ["True1", "True2"]
        predict_list = ["Pred1", "Pred2"]

        mock_ontology = MagicMock()
        gm.ONTO = mock_ontology

        gm.graph_maker("TBox", entity_prefix, individual_list, truth_list, predict_list)

        self.assertTrue(mock_savefig.called)
        self.assertTrue(mock_draw.called)
        self.assertTrue(mock_layout.called)

    @patch("controllers.graph_controller.em.load_individuals")
    @patch("controllers.graph_controller.get_prefix")
    @patch("controllers.graph_controller.graph_maker")
    def test_create_graph(
        self, mock_graph_maker, mock_get_prefix, mock_load_individuals
    ):
        """Test create_graph function in graph_controller.py"""
        id = "test_id"
        mock_load_individuals.return_value = ["Entity1"]
        mock_get_prefix.return_value = "http://example.com#"

        with patch("controllers.graph_controller.load_file") as mock_load_file:
            mock_load_file.return_value = (
                MagicMock(),
                pd.DataFrame(
                    {
                        "Individual": ["Ind1", "Ind2"],
                        "True": ["True1", "True2"],
                        "Predicted": ["Pred1", "Pred2"],
                    }
                ),
            )
            result = gm.create_graph(id)

        self.assertTrue(mock_load_individuals.called)
        self.assertTrue(mock_get_prefix.called)
        self.assertTrue(mock_graph_maker.called)
        self.assertEqual(result, "create graphs success!!")


if __name__ == "__main__":
    unittest.main()
