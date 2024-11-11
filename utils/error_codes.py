from enum import Enum


class ErrorCodes(Enum):
    # GENERAL
    BAD_OBJECT_ID = {
        "error_code": "BAD_OBJECT_ID",
        "message": "El ID proporcionado no es válido."
    }
    # OBJECT NOT FOUND
    OBJECT_NOT_FOUND = {
        "error_code": "OBJECT_NOT_FOUND",
        "message": "No se encontró el registro solicitado."
    }
    #USER PANEL
    USER_NOT_FOUND = {
        "error_code": "USER_PANEL_NOT_FOUND",
        "message": "No se encontró un usuario con ese ID."
    }
    # FORBIDDEN PERMISSION TO ACCESS RESOURCE
    FORBIDDEN = {
        "error_code": "FORBIDDEN",
        "message": "No tienes permiso para acceder a este recurso."
    }
    # COLLECTION NOT FOUND
    COLLECTION_NOT_FOUND = {
        "error_code": "COLLECTION_NOT_FOUND",
        "message": "No se encontró un registro en la colección."
    }
