from fastapi import HTTPException
from starlette import status


class ExceptionHandler(Exception):
    def __init__(self, error_status, error_message):
        self.error_status = error_status
        self.error_message = error_message

    def raise_exception(self):
        if not self.error_status:
            self.error_status = status.HTTP_500_INTERNAL_SERVER_ERROR
        if not self.error_message:
            self.error_message = "Unknown error"
        raise HTTPException(status_code=self.error_status, detail=self.error_message)
