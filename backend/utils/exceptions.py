class CustomException(Exception):
    """Base class for custom exceptions"""

    def __init__(self, message, error_code):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)

    def __str__(self):
        return self.message


class FileException(CustomException):
    """Exception raised for file-related errors"""

    def __init__(self, message="File operation error", error_code=500):
        super().__init__(message, error_code)


class ModelException(CustomException):
    """Exception raised for model-related errors"""

    def __init__(self, message="Model operation error", error_code=500):
        super().__init__(message, error_code)


class EvaluationException(CustomException):
    """Exception raised for evaluation errors"""

    def __init__(self, message="Evaluation failed", error_code=500):
        super().__init__(message, error_code)


class ExtractionException(CustomException):
    """Exception raised for extraction errors"""

    def __init__(self, message="Extraction failed", error_code=500):
        super().__init__(message, error_code)


class GraphException(CustomException):
    """Exception raised for errors related to graph operations"""

    def __init__(self, message="Graph operation error", error_code=500):
        super().__init__(message, error_code)


class OntologyException(CustomException):
    """Exception raised for ontology-related errors"""

    def __init__(self, message="Ontology operation error", error_code=500):
        super().__init__(message, error_code)


class DirectoryException(CustomException):
    """Exception raised for directory-related errors"""

    def __init__(self, message="Directory operation error", error_code=500):
        super().__init__(message, error_code)


# Add more custom exceptions as needed


def handle_exception(e):
    """Utility function to handle exceptions and return appropriate response"""
    if isinstance(e, CustomException):
        return {"message": e.message, "error_code": e.error_code}
    else:
        return {"message": "An unexpected error occurred", "error_code": 500}
