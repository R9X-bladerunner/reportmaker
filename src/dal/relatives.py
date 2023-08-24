from sqlalchemy import select
from sqlalchemy.orm import joinedload

from src.dal.dal import Dal
from src.db.models.tables import Relative, Relationship
from src.schemas.relative import RelativeUpdate
from src.utils.errors import ItemNotFoundError


class RelativeDal(Dal[Relative]):
    model = Relative

    def get_relatives(self) -> list[Relative] | None:   #check None
        filters = select(self.model)
        return self.fetch_all(filters)

    def get_relative_by_id(self, relative_id: int, options = None) -> Relative:
        relative = self.get_(relative_id, options=options)
        if relative is None:
            raise ItemNotFoundError
        return relative

    def get_relative_w_relationship_a_patient(self, relative_id: int):
        relative = self.get_relative_by_id(relative_id, options=[
            joinedload(Relative.relative_association).joinedload(Relationship.relation_patient)])

        return relative


