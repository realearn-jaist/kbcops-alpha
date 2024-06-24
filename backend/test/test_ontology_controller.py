import sys
import unittest
from unittest.mock import MagicMock, mock_open, patch

sys.path.append("../backend")
from owl2vec_star.Onto_Access import Reasoner
from controllers.ontology_controller import (
    extract_data,
    get_onto_stat,
    get_all_ontology,
    upload_ontology,
)


class TestOntologyModule(unittest.TestCase):
    """Test cases for ontology_controller.py"""

    @patch("controllers.ontology_controller.save_ontology")
    def test_upload_ontology_success(self, mock_save_ontology):
        """Test upload_ontology function in ontology_controller.py

        Args:
            mock_save_ontology: MagicMock object
        Returns:
            None
        """
        file = MagicMock()
        id = "test_id.owl"

        mock_save_ontology.return_value = "path/to/test_id.owl"

        result = upload_ontology(file, id)
        self.assertEqual(result, "test_id")

        id = "test_id"
        filename = "test_id.owl"
        mock_save_ontology.assert_called_with(file, id, filename)

    @patch("controllers.ontology_controller.save_ontology")
    def test_upload_ontology_fail(self, mock_save_ontology):
        """Test upload_ontology function in ontology_controller.py

        Args:
            mock_save_ontology: MagicMock object
        Returns:
            None
        """
        file = MagicMock()
        id = "test_id.owl"

        mock_save_ontology.return_value = None

        result = upload_ontology(file, id)
        self.assertEqual(result, None)

        id = "test_id"
        filename = "test_id.owl"
        mock_save_ontology.assert_called_with(file, id, filename)

    @patch("controllers.ontology_controller.list_ontology")
    def test_getAll_ontology(self, mock_list_ontology):
        """Test getAll_ontology function in ontology_controller.py

        Args:
            mock_list_ontology: MagicMock object
        Returns:
            None
        """
        mock_list_ontology.return_value = ["onto1", "onto2"]
        result = get_all_ontology()
        self.assertEqual(result, ["onto1", "onto2"])

    @patch("controllers.ontology_controller.load_axioms")
    @patch("controllers.ontology_controller.load_classes")
    @patch("controllers.ontology_controller.load_individuals")
    @patch("controllers.ontology_controller.load_annotations")
    def test_get_onto_stat(
        self,
        mock_load_annotations,
        mock_load_individuals,
        mock_load_classes,
        mock_load_axioms,
    ):
        """Test get_onto_stat function in ontology_controller.py

        Args:
            mock_load_annotations: MagicMock object
            mock_load_individuals: MagicMock object
            mock_load_classes: MagicMock object
            mock_load_axioms: MagicMock object
        Returns:
            None
        """
        mock_load_axioms.return_value = ["axiom1", "axiom2"]
        mock_load_classes.return_value = ["class1", "class2"]
        mock_load_individuals.return_value = ["ind1", "ind2"]
        mock_load_annotations.return_value = (
            ["uri1 label1", "uri2 label2 label3"],
            ["uri1 annotation1", "uri2 annotation2"],
        )

        id = "test_id"
        result = get_onto_stat(id)
        self.assertEqual(
            result,
            {"no_class": 2, "no_individual": 2, "no_axiom": 2, "no_annotation": 4},
        )

    @patch("controllers.ontology_controller.get_path_ontology")
    @patch("controllers.ontology_controller.OntologyProjection")
    @patch("controllers.ontology_controller.save_axioms")
    @patch("controllers.ontology_controller.save_classes")
    @patch("controllers.ontology_controller.save_individuals")
    @patch("controllers.ontology_controller.save_annotations")
    @patch("controllers.ontology_controller.get_ontology")
    @patch("controllers.ontology_controller.tbox_infer")
    @patch("controllers.ontology_controller.abox_infer")
    @patch("controllers.ontology_controller.save_infer")
    @patch("controllers.ontology_controller.load_classes")
    @patch("controllers.ontology_controller.load_individuals")
    @patch("controllers.ontology_controller.train_test_val_abox")
    @patch("controllers.ontology_controller.train_test_val_tbox")
    def test_extract_data(
        self,
        mock_train_test_val_tbox,
        mock_train_test_val_abox,
        mocl_load_individuals,
        mock_load_classes,
        mock_save_infer,
        mock_abox_infer,
        mock_tbox_infer,
        mock_get_ontology,
        mock_save_annotations,
        mock_save_individuals,
        mock_save_classes,
        mock_save_axioms,
        mock_OntologyProjection,
        mock_get_path_ontology,
    ):
        """Test extract_data function in ontology_controller.py

        Args:
            mock_train_test_val_tbox: MagicMock object
            mock_train_test_val_abox: MagicMock object
            mocl_load_individuals: MagicMock object
            mock_load_classes: MagicMock object
            mock_save_infer: MagicMock object
            mock_abox_infer: MagicMock object
            mock_tbox_infer: MagicMock object
            mock_get_ontology: MagicMock object
            mock_save_annotations: MagicMock object
            mock_save_individuals: MagicMock object
            mock_save_classes: MagicMock object
            mock_save_axioms: MagicMock object
            mock_OntologyProjection: MagicMock object
            mock_get_path_ontology: MagicMock object
        Returns:
            None
        """
        mock_get_path_ontology.return_value = "path_to_ontology"
        mock_get_ontology.return_value = MagicMock()
        mock_projection_instance = MagicMock()
        mock_OntologyProjection.return_value = mock_projection_instance
        mock_abox_infer.return_value = []
        mock_tbox_infer.return_value = []
        mock_save_infer.return_value = None
        mocl_load_individuals.return_value = {"ind1", "ind2"}
        mock_load_classes.return_value = {"class1", "class2"}
        mock_train_test_val_tbox.return_value = None
        mock_train_test_val_abox.return_value = None

        mock_projection_instance.createManchesterSyntaxAxioms.return_value = None
        mock_projection_instance.axioms_manchester = ["axiom1", "axiom2"]
        mock_projection_instance.getClassURIs.return_value = {"class1", "class2"}
        mock_projection_instance.getIndividualURIs.return_value = {"ind1", "ind2"}
        mock_projection_instance.entityToPreferredLabels = {
            "class1": {"Label1"},
            "ind1": {"Label2"},
        }
        mock_projection_instance.entityToAllLexicalLabels = {
            "class1": {"Label1"},
            "ind1": {"Label2"},
            "ind2": {"Label3"},
        }

        mock_save_axioms.return_value = ["axiom1", "axiom2"]
        mock_save_classes.return_value = {"class1", "class2"}
        mock_save_individuals.return_value = {"ind1", "ind2"}
        mock_save_annotations.return_value = [
            ["class1", "Label1"],
            ["ind1", "Label2"],
            ["ind2", "Label3"],
        ]

        id = "test_id"
        result = extract_data(id)

        self.assertEqual(
            result,
            {"no_class": 2, "no_individual": 2, "no_axiom": 2, "no_annotation": 3},
        )
        mock_get_path_ontology.assert_any_call(id)
        mock_OntologyProjection.assert_called_once_with(
            "path_to_ontology",
            reasoner=Reasoner.STRUCTURAL,
            only_taxonomy=False,
            bidirectional_taxonomy=True,
            include_literals=True,
            avoid_properties=set(),
            additional_preferred_labels_annotations=set(),
            additional_synonyms_annotations=set(),
            memory_reasoner="13351",
        )
        mock_save_axioms.assert_called_once_with(id, ["axiom1", "axiom2"])
        mock_save_classes.assert_called_once_with(id, {"class1", "class2"})
        mock_save_individuals.assert_called_once_with(id, {"ind1", "ind2"})
        self.assertTrue(mock_save_annotations.called)


if __name__ == "__main__":
    unittest.main()
