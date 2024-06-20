import sys
import unittest
from io import BytesIO
from unittest.mock import patch

sys.path.append('../backend')
from app import create_app


class TestOntologyUpload(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.app = create_app()
        self.app.testing = True
        self.app = self.app.test_client()

    @patch("routes.routes.upload_ontology")
    def test_upload_success_idWithOwl(self, mock_upload_ontology):
        """Test that the upload route works successfully when a file is uploaded"""
        data = {
            "owl_file": (BytesIO(b"mock owl data"), "test.owl"),
            "onto_id": "test_id.owl",
        }
        mock_upload_ontology.return_value = "test_id"
        response = self.app.post(
            "/upload", data=data, content_type="multipart/form-data"
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("File uploaded successfully", response.get_json()["message"])
        self.assertIn("test_id", response.get_json()["onto_id"])
        
    @patch("routes.routes.upload_ontology")
    def test_upload_success_idWithoutOwl(self, mock_upload_ontology):
        """Test that the upload route works successfully when a file is uploaded"""
        data = {
            "owl_file": (BytesIO(b"mock owl data"), "test.owl"),
            "onto_id": "test_id",
        }
        mock_upload_ontology.return_value = "test_id"
        response = self.app.post(
            "/upload", data=data, content_type="multipart/form-data"
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("File uploaded successfully", response.get_json()["message"])
        self.assertIn("test_id", response.get_json()["onto_id"])

    @patch("routes.routes.upload_ontology")
    def test_upload_failure_cannot_upload(self, mock_upload_ontology):
        """Test that the upload route fails when the file cannot be uploaded"""
        mock_upload_ontology.return_value = None  # Ensure upload_ontology returns None

        data = {
            "owl_file": (BytesIO(b"mock owl data"), "test.owl"),
            "onto_id": "test_id.owl",
        }
        response = self.app.post(
            "/upload", data=data, content_type="multipart/form-data"
        )
        self.assertEqual(response.status_code, 500)
        self.assertIn("File upload failed", response.get_json()["message"])

    def test_upload_failure_no_file(self):
        """Test that the upload route fails when no file is uploaded"""
        data = {"onto_id": "test_id.owl"}
        response = self.app.post(
            "/upload", data=data, content_type="multipart/form-data"
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("No file part", response.get_json()["message"])

    @patch("routes.routes.extract_data")
    def test_extract_success(self, mock_extract_data):
        """Test that the extract route works successfully when data is extracted"""
        mock_extract_data.return_value = {
            "no_class": 1,
            "no_individual": 2,
            "no_axiom": 3,
            "no_annotation": 4,
        }
        response = self.app.get("/extract/test_ontology.owl")

        # Assert the status code
        self.assertEqual(response.status_code, 200)

        # Assert the message
        self.assertIn("Extraction successfully", response.get_json()["message"])
        self.assertEqual({
            "no_class": 1,
            "no_individual": 2,
            "no_axiom": 3,
            "no_annotation": 4,
        }, response.get_json()["data"])

    # Extract data mock is no longer active outside the `with` block

    @patch("routes.routes.extract_data")
    def test_extract_failure(self, mock_extract_data):
        """Test that the extract route fails when data extraction fails"""
        mock_extract_data.return_value = None
        response = self.app.get("/extract/test_ontology")
        self.assertEqual(response.status_code, 500)
        self.assertIn("Extraction failed", response.get_json()["message"])

    @patch("routes.routes.getAll_ontology")
    def test_list_ontologies(self, mock_getAll_ontology):
        """Test that the list_ontologies route works successfully when ontologies are listed successfully"""
        mock_getAll_ontology.return_value = ["ontology1", "ontology2"]
        response = self.app.get("/ontology")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Ontologies listed successfully", response.get_json()["message"])
        self.assertEqual(["ontology1", "ontology2"], response.get_json()["onto_list"])
    
    @patch("routes.routes.get_onto_stat")
    def test_get_ontology_stat(self, mock_get_onto_stat):
        """Test that the get_ontology_stat route works successfully when can return ontology stats successfully"""
        mock_get_onto_stat.return_value = {
            "no_class": 0,
            "no_individual": 1,
            "no_axiom": 2,
            "no_annotation": 3,
        }
        response = self.app.get("/ontology/test_ontology")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Ontologies listed successfully", response.get_json()["message"])
        self.assertEqual({
            "no_class": 0,
            "no_individual": 1,
            "no_axiom": 2,
            "no_annotation": 3,
        }, response.get_json()["data"])

    @patch("routes.routes.embed_func")
    def test_embed_route_model_exists(self, mock_embed_func):
        """Test that the embed route returns a message indicating that the model already exists if the model exists"""
        mock_embed_func.return_value = "test_algo model already exists for test_ontology ontology"
        with patch("os.path.exists") as mock_exists:
            mock_exists.return_value = True
            response = self.app.get("/embed/test_ontology?algo=test_algo")
            self.assertEqual(response.status_code, 200)
            self.assertIn("test_algo model already exists for test_ontology ontology", response.get_json()["message"])

    @patch("routes.routes.embed_func")
    def test_embed_route_generate_model(self, mock_embed_func):
        """Test that the embed route generates a model if the model does not exist"""
        mock_embed_func.return_value = "test_algo embedded success!!"
        with patch("os.path.exists") as mock_exists:
            mock_exists.return_value = False
            response = self.app.get("/embed/test_ontology?algo=test_algo")
            print("embed re", response.get_json())
            self.assertEqual(response.status_code, 200)
            self.assertIn("test_algo embedded success!!", response.get_json()["message"])
            self.assertIn("test_ontology", response.get_json()["onto_id"])
            self.assertIn("test_algo", response.get_json()["algo"])

    @patch("routes.routes.predict_func")
    def test_predict_route(self, mock_predict_func):
        """Test that the predict route returns the prediction result"""
        mock_predict_func.return_value = {
            "message": "evaluate successful!",
            "performance": {
                    'Individual': 0, 
                    'Predicted': 1, 
                    'Predicted_rank': 2, 
                    'True': 3, 
                    'True_rank' : 4, 
                    'Score_predict': 5, 
                    'Score_true': 6,
                    'Dif': 7 
                },
            "garbage": [],
            "images": []
        }
        response = self.app.get("/evaluate/test_ontology/test_model")
        print("predict re", response.get_json())
        self.assertEqual(response.status_code, 200)
        self.assertIn("evaluate successful!", response.get_json()["message"])
        self.assertEqual({
                    'Individual': 0, 
                    'Predicted': 1, 
                    'Predicted_rank': 2, 
                    'True': 3, 
                    'True_rank' : 4, 
                    'Score_predict': 5, 
                    'Score_true': 6,
                    'Dif': 7 
                }, response.get_json()["performance"])
        self.assertEqual([], response.get_json()["garbage"])
        self.assertEqual([], response.get_json()["images"])
        self.assertEqual(len(response.get_json()["images"]), len(response.get_json()["garbage"]))


if __name__ == "__main__":
    unittest.main()