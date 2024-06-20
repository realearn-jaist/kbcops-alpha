import sys
import unittest
from unittest.mock import MagicMock, patch

sys.path.append('../backend')
from owl2vec_star.Onto_Access import Reasoner
from controllers.ontology_controller import extract_data, get_onto_stat, getAll_ontology, upload_ontology


class TestOntologyModule(unittest.TestCase):

    @patch("controllers.ontology_controller.save_ontology")
    def test_upload_ontology_success(self, mock_save_ontology):
        """Test upload_ontology function in ontology_controller.py"""
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
        """Test upload_ontology function in ontology_controller.py"""
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
        """Test getAll_ontology function in ontology_controller.py"""
        mock_list_ontology.return_value = ["onto1", "onto2"]
        result = getAll_ontology()
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
        """Test get_onto_stat function in ontology_controller.py"""
        mock_load_axioms.return_value = ["axiom1", "axiom2"]
        mock_load_classes.return_value = set(["class1", "class2"])
        mock_load_individuals.return_value = set(["ind1", "ind2"])
        mock_load_annotations.return_value = ["ann1", "ann2"]

        id = "test_id"
        result = get_onto_stat(id)
        self.assertEqual(
            result,
            {"no_class": 2, "no_individual": 2, "no_axiom": 2, "no_annotation": 2},
        )

    @patch("controllers.ontology_controller.getPath_ontology")
    @patch("controllers.ontology_controller.OntologyProjection")
    @patch("controllers.ontology_controller.save_axioms")
    @patch("controllers.ontology_controller.save_classes")
    @patch("controllers.ontology_controller.save_individuals")
    @patch("controllers.ontology_controller.save_annotations")
    def test_extract_data(
        self,
        mock_save_annotations,
        mock_save_individuals,
        mock_save_classes,
        mock_save_axioms,
        mock_OntologyProjection,
        mock_getPath_ontology,
    ):
        """Test extract_data function in ontology_controller.py"""
        mock_getPath_ontology.return_value = "path_to_ontology"
        mock_projection_instance = MagicMock()
        mock_OntologyProjection.return_value = mock_projection_instance

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
        mock_getPath_ontology.assert_called_once_with(id)
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