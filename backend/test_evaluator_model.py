import unittest
from unittest.mock import MagicMock, call, mock_open, patch

from models.evaluator_model import (
    read_garbage_metrics,
    read_json_file,
    write_garbage_metrics,
    write_json_file,
)


class TestFileOperations(unittest.TestCase):

    @patch("models.evaluator_model.getPath_ontology_directory")
    @patch("builtins.open", new_callable=mock_open)
    def test_write_json_file(self, mock_open, mock_getPath):
        """Test write_json_file function in evaluator_model.py"""
        mock_getPath.return_value = "\\fake\\path"
        data = {"key": "value"}

        write_json_file("ontology", "algorithm", data)

        mock_open.assert_called_once_with(
            "\\fake\\path\\algorithm\\performance.json", "w"
        )
        calls = [
            call("{"),
            call("\n    "),
            call('"key"'),
            call(": "),
            call('"value"'),
            call("\n"),
            call("}"),
        ]
        mock_open().write.assert_has_calls(calls)

    @patch("models.evaluator_model.getPath_ontology_directory")
    @patch("builtins.open", new_callable=mock_open, read_data='{"key": "value"}')
    def test_read_json_file(self, mock_open, mock_getPath):
        """Test read_json_file function in evaluator_model.py"""
        mock_getPath.return_value = "\\fake\\path"

        result = read_json_file("ontology", "algorithm")

        mock_open.assert_called_once_with(
            "\\fake\\path\\algorithm\\performance.json", "r"
        )
        self.assertEqual(result, {"key": "value"})

    @patch("models.evaluator_model.getPath_ontology_directory")
    @patch("builtins.open", new_callable=mock_open)
    @patch("csv.DictWriter")
    def test_write_garbage_metrics(self, mock_csv_dictwriter, mock_open, mock_getPath):
        """Test write_garbage_metrics function in evaluator_model.py"""
        mock_getPath.return_value = "\\fake\\path"
        data = [
            {
                "Individual": "A",
                "Predicted": "B",
                "Predicted_rank": "1",
                "True": "C",
                "True_rank": "2",
                "Score_predict": "0.9",
                "Score_true": "0.8",
                "Dif": "0.1",
            }
        ]

        mock_writer_instance = MagicMock()
        mock_csv_dictwriter.return_value = mock_writer_instance

        write_garbage_metrics("ontology", "algorithm", data)

        mock_open.assert_called_once_with(
            "\\fake\\path\\algorithm\\garbage.csv", "w", newline=""
        )
        mock_writer_instance.writeheader.assert_called_once()
        mock_writer_instance.writerows.assert_called_once_with(data)

    @patch("models.evaluator_model.getPath_ontology_directory")
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="Individual,Predicted,Predicted_rank,True,True_rank,Score_predict,Score_true,Dif\nA,B,1,C,2,0.9,0.8,0.1\n",
    )
    def test_read_garbage_metrics(self, mock_open, mock_getPath):
        """Test read_garbage_metrics function in evaluator_model.py"""
        mock_getPath.return_value = "\\fake\\path"

        result = read_garbage_metrics("ontology", "algorithm")

        mock_open.assert_called_once_with(
            "\\fake\\path\\algorithm\\garbage.csv", mode="r", newline=""
        )
        self.assertEqual(
            result,
            [
                {
                    "Individual": "A",
                    "Predicted": "B",
                    "Predicted_rank": "1",
                    "True": "C",
                    "True_rank": "2",
                    "Score_predict": "0.9",
                    "Score_true": "0.8",
                    "Dif": "0.1",
                }
            ],
        )


if __name__ == "__main__":
    unittest.main()
