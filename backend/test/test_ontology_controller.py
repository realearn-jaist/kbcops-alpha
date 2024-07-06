import sys
import unittest
from unittest.mock import MagicMock, mock_open, patch

from utils.exceptions import OntologyException

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

        # Configure the mock to return None to simulate failure
        mock_save_ontology.return_value = None

        # Ensure that the upload_ontology function raises the OntologyException
        with self.assertRaises(OntologyException) as context:
            upload_ontology(file, id)

        self.assertEqual(str(context.exception), "Failed to save ontology file")

        # Ensure the correct call was made
        id = "test_id"
        filename = "test_id.owl"
        mock_save_ontology.assert_called_with(file, id, filename)

    @patch("controllers.ontology_controller.list_ontology")
    def test_getAll_ontology(self, mock_list_ontology):
        """Test get_all_ontology function in ontology_controller.py

        Args:
            mock_list_ontology: MagicMock object
        Returns:
            None
        """
        mock_list_ontology.return_value = ["onto1", "onto2"]
        result = get_all_ontology()
        self.assertEqual(result, ["onto1", "onto2"])

    @patch(
        "controllers.ontology_controller.load_multi_input_files",
        return_value={
            "axioms": ["axiom1", "axiom2"],
            "classes": ["class1", "class2"],
            "individuals": ["individual1", "individual2"],
            "uri_labels": ["uri1 label1", "uri2 label2 label3"],
            "annotations": ["uri1 annotation1", "uri2 annotation2"],
        },
    )
    def test_get_onto_stat(
        self,
        mock_load_multi_input_files,
    ):
        """Test get_onto_stat function in ontology_controller.py

        Args:
            mock_load_multi_input_files: MagicMock object
        Returns:
            None
        """

        id = "ontology_name"
        result = get_onto_stat(id)
        self.assertEqual(
            result,
            {"no_class": 2, "no_individual": 2, "no_axiom": 2, "no_annotation": 4},
        )

        mock_load_multi_input_files.assert_called_once_with(
            "ontology_name",
            ["axioms", "classes", "individuals", "uri_labels", "annotations"],
        )

    @patch("controllers.ontology_controller.train_test_val_gen_abox")
    @patch("controllers.ontology_controller.train_test_val_gen_tbox")
    @patch("controllers.ontology_controller.load_multi_input_files")
    @patch("controllers.ontology_controller.save_infer")
    @patch("controllers.ontology_controller.abox_infer")
    @patch("controllers.ontology_controller.tbox_infer")
    @patch("controllers.ontology_controller.World")
    @patch("controllers.ontology_controller.save_annotations")
    @patch("controllers.ontology_controller.save_individuals")
    @patch("controllers.ontology_controller.save_classes")
    @patch("controllers.ontology_controller.save_axioms")
    @patch("controllers.ontology_controller.OntologyProjection")
    @patch("controllers.ontology_controller.get_path")
    def test_extract_data(
        self,
        mock_get_path,
        mock_OntologyProjection,
        mock_save_axioms,
        mock_save_classes,
        mock_save_individuals,
        mock_save_annotations,
        mock_World,
        mock_tbox_infer,
        mock_abox_infer,
        mock_save_infer,
        mock_load_multi_input_files,
        mock_train_test_val_gen_tbox,
        mock_train_test_val_gen_abox,
    ):
        """Test extract_data function in ontology_controller.py

        Args:
            mock_get_path: MagicMock object
            mock_OntologyProjection: MagicMock object
            mock_save_axioms: MagicMock object
            mock_save_classes: MagicMock object
            mock_save_individuals: MagicMock object
            mock_save_annotations: MagicMock object
            mock_World: MagicMock object
            mock_tbox_infer: MagicMock object
            mock_abox_infer: MagicMock object
            mock_save_infer: MagicMock object
            mock_load_multi_input_files: MagicMock object
            mock_train_test_val_gen_tbox: MagicMock object
            mock_train_test_val_gen_abox: MagicMock object
        Returns:
            None
        """

        # Setup mocks
        mock_get_path.return_value = "path_to_ontology"
        mock_world_instance = MagicMock()
        mock_World.return_value = mock_world_instance
        mock_ontology_instance = MagicMock()
        mock_world_instance.get_ontology.return_value = mock_ontology_instance
        mock_ontology_instance.load.return_value = mock_ontology_instance

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
        mock_abox_infer.return_value = []
        mock_tbox_infer.return_value = []
        mock_save_infer.return_value = None
        mock_train_test_val_gen_tbox.return_value = None
        mock_train_test_val_gen_abox.return_value = None

        mock_load_multi_input_files.return_value = {
            "classes": {"class1", "class2"},
            "individuals": {"ind1", "ind2"},
        }

        # Call the function
        ontology_name = "ontology_name"
        result = extract_data(ontology_name)

        # Assert results
        self.assertEqual(
            result,
            {
                "no_class": 2,
                "no_individual": 2,
                "no_axiom": 2,
                "no_annotation": 3,
            },
        )

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
        mock_World.assert_called_once()
        mock_world_instance.get_ontology.assert_called_once_with("path_to_ontology")
        mock_ontology_instance.load.assert_called_once()
        mock_load_multi_input_files.assert_called_once_with(
            ontology_name, ["classes", "individuals"]
        )
        mock_save_axioms.assert_called_once_with(ontology_name, ["axiom1", "axiom2"])
        mock_save_classes.assert_called_once_with(ontology_name, {"class1", "class2"})
        mock_save_individuals.assert_called_once_with(ontology_name, {"ind1", "ind2"})
        self.assertTrue(mock_save_annotations.called)


if __name__ == "__main__":
    unittest.main()
