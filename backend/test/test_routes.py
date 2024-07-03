import sys
import unittest
from io import BytesIO
from unittest.mock import patch

sys.path.append("../backend")
from main import create_app


class TestRoutes(unittest.TestCase):
    """Test cases for routes.py"""

    @classmethod
    def setUp(self):
        """Create the Flask app and a test client for the app. Establish an application context before each test.
        Args:
            self: TestRoutes object
        Returns:
            None
        """
        self.app = create_app()
        self.app.testing = True
        self.app = self.app.test_client()

    @patch("routes.routes.upload_ontology")
    def test_upload_success_idWithOwl(self, mock_upload_ontology):
        """Test that the upload route works successfully when a file is uploaded

        Args:
            mock_upload_ontology: MagicMock object
        Returns:
            None
        """
        data = {
            "owl_file": (BytesIO(b"mock owl data"), "test.owl"),
            "ontology_name": "test_id.owl",
            "alias": "test_alias",
        }
        mock_upload_ontology.return_value = "test_id"
        response = self.app.post(
            "/api/upload", data=data, content_type="multipart/form-data"
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("File uploaded successfully", response.get_json()["message"])
        self.assertIn("test_id", response.get_json()["ontology_name"])

    @patch("routes.routes.upload_ontology")
    def test_upload_success_idWithoutOwl(self, mock_upload_ontology):
        """Test that the upload route works successfully when a file is uploaded

        Args:
            mock_upload_ontology: MagicMock object
        Returns:
            None
        """
        data = {
            "owl_file": (BytesIO(b"mock owl data"), "test.owl"),
            "ontology_name": "test_id",
            "alias": "test_alias",
        }
        mock_upload_ontology.return_value = "test_id"
        response = self.app.post(
            "/api/upload", data=data, content_type="multipart/form-data"
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("File uploaded successfully", response.get_json()["message"])
        self.assertIn("test_id", response.get_json()["ontology_name"])

    @patch("routes.routes.remove_dir")
    @patch("routes.routes.upload_ontology")
    def test_upload_failure_cannot_upload(self, mock_upload_ontology, mock_remove_dir):
        """Test that the upload route fails when the file cannot be uploaded

        Args:
            mock_upload_ontology: MagicMock object
        Returns:
            None
        """
        mock_upload_ontology.return_value = None  # Ensure upload_ontology returns None
        mock_remove_dir.return_value = None  # Ensure remove_dir returns None
        data = {
            "owl_file": (BytesIO(b"mock owl data"), "test.owl"),
            "ontology_name": "test_id.owl",
            "alias": "test_alias",
        }
        response = self.app.post(
            "/api/upload", data=data, content_type="multipart/form-data"
        )
        self.assertEqual(response.status_code, 500)

    def test_upload_failure_no_file(self):
        """Test that the upload route fails when no file is uploaded

        Args:
            self: TestRoutes object
        Returns:
            None
        """
        data = {"ontology_name": "test_id.owl"}
        response = self.app.post(
            "/api/upload", data=data, content_type="multipart/form-data"
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("No file part", response.get_json()["message"])

    @patch("routes.routes.extract_data")
    def test_extract_success(self, mock_extract_data):
        """Test that the extract route works successfully when data is extracted

        Args:
            mock_extract_data: MagicMock object
        Returns:
            None
        """
        mock_extract_data.return_value = {
            "no_class": 1,
            "no_individual": 2,
            "no_axiom": 3,
            "no_annotation": 4,
        }
        response = self.app.get("/api/extract/test_ontology.owl")

        # Assert the status code
        self.assertEqual(response.status_code, 200)

        # Assert the message
        self.assertIn("Extraction successfully", response.get_json()["message"])
        self.assertEqual(
            {
                "no_class": 1,
                "no_individual": 2,
                "no_axiom": 3,
                "no_annotation": 4,
            },
            response.get_json()["onto_data"],
        )

    # Extract data mock is no longer active outside the `with` block

    @patch("routes.routes.extract_data")
    def test_extract_failure(self, mock_extract_data):
        """Test that the extract route fails when data extraction fails

        Args:
            mock_extract_data: MagicMock object
        Returns:
            None
        """
        mock_extract_data.return_value = None
        response = self.app.get("/api/extract/test_ontology")
        self.assertEqual(response.status_code, 500)

    @patch("routes.routes.get_all_ontology")
    def test_list_ontologies(self, mock_get_all_ontology):
        """Test that the list_ontologies route works successfully when ontologies are listed successfully

        Args:
            mock_getAll_ontology: MagicMock object
        Returns:
            None
        """
        mock_get_all_ontology.return_value = ["ontology1", "ontology2"]
        response = self.app.get("/api/ontology")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Ontologies listed successfully", response.get_json()["message"])
        self.assertEqual(["ontology1", "ontology2"], response.get_json()["onto_list"])

    @patch("routes.routes.get_onto_stat")
    def test_get_ontology_stat(self, mock_get_onto_stat):
        """Test that the get_ontology_stat route works successfully when can return ontology stats successfully

        Args:
            mock_get_onto_stat: MagicMock object
        Returns:
            None
        """
        mock_get_onto_stat.return_value = {
            "no_class": 0,
            "no_individual": 1,
            "no_axiom": 2,
            "no_annotation": 3,
        }
        response = self.app.get("/api/ontology/test_ontology")
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "load Ontologies Stats successfully", response.get_json()["message"]
        )
        self.assertEqual(
            {
                "no_class": 0,
                "no_individual": 1,
                "no_axiom": 2,
                "no_annotation": 3,
            },
            response.get_json()["onto_data"],
        )

    @patch("routes.routes.embed_func")
    def test_embed_route_model_exists(self, mock_embed_func):
        """Test that the embed route returns a message indicating that the model already exists if the model exists

        Args:
            mock_embed_func: MagicMock object
        Returns:
            None
        """
        mock_embed_func.return_value = (
            "test_algo model already exists for test_ontology ontology"
        )
        with patch("os.path.exists") as mock_exists:
            mock_exists.return_value = True
            response = self.app.get("/api/embed/test_ontology?algo=test_algo")
            self.assertEqual(response.status_code, 200)
            self.assertIn(
                "test_algo model already exists for test_ontology ontology",
                response.get_json()["message"],
            )

    @patch("routes.routes.embed_func")
    def test_embed_route_generate_model(self, mock_embed_func):
        """Test that the embed route generates a model if the model does not exist

        Args:
            mock_embed_func: MagicMock object
        Returns:
            None
        """
        mock_embed_func.return_value = "test_algo embedded success!!"
        with patch("os.path.exists") as mock_exists:
            mock_exists.return_value = False
            response = self.app.get("/api/embed/test_ontology?algo=test_algo")

            self.assertEqual(response.status_code, 200)
            self.assertIn(
                "test_algo embedded success!!", response.get_json()["message"]
            )
            self.assertIn("test_ontology", response.get_json()["ontology_name"])
            self.assertIn("test_algo", response.get_json()["algo"])

    @patch("routes.routes.predict_func")
    def test_predict_route(self, mock_predict_func):
        """Test that the predict route returns the prediction result

        Args:
            mock_predict_func: MagicMock object
        Returns:
            None
        """
        mock_predict_func.return_value = {
            "message": "evaluate successful!",
            "performance": {
                "Individual": 0,
                "Predicted": 1,
                "Predicted_rank": 2,
                "True": 3,
                "True_rank": 4,
                "Score_predict": 5,
                "Score_true": 6,
                "Dif": 7,
            },
            "garbage": [],
            "images": [],
        }
        response = self.app.get(
            "/api/evaluate/test_ontology/test_model/test_classifier"
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("evaluate successful!", response.get_json()["message"])
        self.assertEqual(
            {
                "Individual": 0,
                "Predicted": 1,
                "Predicted_rank": 2,
                "True": 3,
                "True_rank": 4,
                "Score_predict": 5,
                "Score_true": 6,
                "Dif": 7,
            },
            response.get_json()["performance"],
        )
        self.assertEqual([], response.get_json()["garbage"])
        self.assertEqual([], response.get_json()["images"])
        self.assertEqual(
            len(response.get_json()["images"]), len(response.get_json()["garbage"])
        )


if __name__ == "__main__":
    unittest.main()
