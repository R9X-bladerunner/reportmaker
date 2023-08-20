
from fastapi import HTTPException, status


class BaseError(HTTPException):
    code: int
    message: str
    headers: dict | None = None

    def __init__(self) -> None:
        super().__init__(self.code, self.message, self.headers)


# ----------------------------------- shared ---------------------------------


class FkNotFoundError(BaseError):
    code = status.HTTP_404_NOT_FOUND
    message = "Can't find FK with given ID"


class ItemNotFoundError(BaseError):
    code = status.HTTP_404_NOT_FOUND
    message = "Can't find item"


class ValidationError(BaseError):
    code = status.HTTP_422_UNPROCESSABLE_ENTITY
    message = 'Unprocessable entity'


class RecordAlreadyExistError(BaseError):
    code = status.HTTP_422_UNPROCESSABLE_ENTITY
    message = 'Record already exist'

