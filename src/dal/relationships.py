from sqlalchemy import select

from src.dal.dal import Dal
from src.db.models.tables import Relationship
from src.schemas.relative import RelativeIn
from src.utils.errors import ItemNotFoundError
from sqlalchemy import and_


class RelationshipDal(Dal[Relationship]):
    model = Relationship
    def get_relation(self, patient_id: int, relative_id:int) -> Relationship:
        stmt = select(self.model).where(
            and_(
                self.model.patient_id == patient_id,
               self.model.relative_id == relative_id
            )
        )
        result = self.sess.execute(stmt)
        relation = result.unique().fetchone()
        print(f'-  ------------------{relation}')
        if relation is None:
            raise ItemNotFoundError
        return relation
