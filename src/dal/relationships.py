from src.db.models.tables import relationships
from src.schemas.patient import PatientIn, PatientUpdate
from src.schemas.relative import RelativeIn
from src.utils.errors import RecordAlreadyExistError
from sqlalchemy import delete, insert, select, update, and_

from collections.abc import Mapping
from  src.dal.dal import Dal

class RelationshipsDal(Dal[relationships]):
    model = relationships
