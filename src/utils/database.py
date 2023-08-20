from contextlib import contextmanager
from dataclasses import dataclass

from sqlalchemy.exc import IntegrityError

from errors import FkNotFoundError, RecordAlreadyExistError


@dataclass(frozen=True, slots=True)
class PostgreErrorHandler:
    pgcode: str
    exc: type[Exception]

    @contextmanager
    def __call__(self, exception: type[Exception] | None = None):
        try:
            yield
        except IntegrityError as exc:
            if hasattr(exc.orig, 'pgcode') and exc.orig.pgcode == self.pgcode:
                raise exception or self.exc
            raise


handle_fk_violation = PostgreErrorHandler('23503', FkNotFoundError)
handle_unique_violation = PostgreErrorHandler('23505', RecordAlreadyExistError)