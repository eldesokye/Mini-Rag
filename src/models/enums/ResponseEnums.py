from enum import Enum

class ResponseSignal(Enum):

    FILE_TYPE_NOT_ALLOWED = "file type not allowed"
    FILE_SIZE_EXCEEDS_LIMIT = "file size exceeds limit"
    FILE_UPLOAD_SUCCESS = "file uploaded successfully"
    FILE_UPLOAD_FAILED = "file upload failed"
    FILE_VALIDATION_SUCCESS = "file is valid"
    FILE_VALIDATION_FAILED = "file is invalid"
    FILE_PROCESSING_FAILED = "file processing failed"
    FILE_PROCESSING_SUCCESS = "file processed successfully"
    NO_FILES_ERROR ="no_found_files"
    