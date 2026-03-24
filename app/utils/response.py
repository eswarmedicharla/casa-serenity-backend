from fastapi import status

def success_response(data=None, message="Success", code=status.HTTP_200_OK):
    return {
        "status": "success",
        "code": code,
        "message": message,
        "data": data
    }

def error_response(message="Error", code=status.HTTP_400_BAD_REQUEST):
    return {
        "status": "error",
        "code": code,
        "message": message,
        "data": None
    }