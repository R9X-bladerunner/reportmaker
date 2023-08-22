from sqlalchemy import select, and_

from src.dal.dal import Dal
from ..db.models.tables import Patient, Relative, relationships
from ..schemas.patient import PatientIn, PatientUpdate
from ..schemas.relative import RelativeIn
from ..utils.errors import ItemNotFoundError


class PatientDal(Dal[Patient]):
    model = Patient

    def get_patients(self) -> list[Patient] | None:
        filters = select(self.model)
        return self.fetch_all(filters)


    def get_patient_by_id(self, patient_id: int) -> Patient | None:
        patient = self.get_(patient_id)
        if patient is None:
            raise ItemNotFoundError

        return patient


    def create(self, schema: PatientIn) -> Patient:
        patient = Patient(**schema.dict())
        return self.add_orm(patient)

    #
    def update_by_id(self, patient_id: int, data: PatientUpdate) -> Patient:
        filters = {'id': patient_id}
        patch = data.dict(exclude_unset=True)
        updated_patient = self.update(filters, patch)
        if updated_patient is None:
            raise ItemNotFoundError   #   Посмотреть что должно возвращаться по соглашению
        return self.update(filters, patch)


    def delete_by_id(self, patient_id: int) -> None:
        patient = self.get_(patient_id)
        if patient is None:
            raise ItemNotFoundError

        self.delete_orm(patient)

        for relative in patient.relatives:
            if len(relative.patients) == 1:
                self.delete_orm(relative)

        return None

    def create_relative(self, patient_id: int, relative_data: RelativeIn) -> Relative:
        patient = self.get_patient_by_id(patient_id)
        if patient is None:
            raise ItemNotFoundError

        relative = Relative(**relative_data.dict(exclude={'relationship_type'}))
        patient.relatives.append(relative)
        self.sess.flush()
        self.sess.execute(
            relationships.update()
            .values(relationship_type=relative_data.relationship_type)
            .where(
                and_(
                    relationships.c.patient_id == patient_id,
                    relationships.c.relative_id == relative.id
                )
            )
        )

        return relative

    def get_relatives(self, patient_id: int) -> list[Relative]:

        patient = self.get_patient_by_id(patient_id)
        relatives = patient.relatives
        return relatives








    # def delete_patient_with_relatives(dal, patient_id):
    #         patient = dal.get_(patient_id)
    #
    #         if patient is None:
    #             return
    #
    #         # Удаление пациента
    #         dal.delete_orm(patient)
    #
    #         # Удаление родственников пациента без связей с другими пациентами
    #         for relative in patient.relatives:
    #             if len(relative.patients) == 1:
    #                 dal.delete_orm(relative)

    #
    # def get_all_or_limit (self, limit: int = None) -> list[Patient] | None:
    #
    #     stmt = select(self.model).where(self.model.is_patient == True)
    #     return self.fetch_all()
    #
    #
    # def delete_patient(self):
    #     pass

    # async def publish(self, route_id: Uid, user: User) -> int:
    #     stmt = update(Route).filter_by(
    #         id=route_id,
    #         is_active=True,
    #         user_id=user.id,
    #     ).values(is_public=True)
    #     return await self.update_n(stmt)
    # async def bulk_get(self, ids: Sequence[Uid]) -> list[Route]:
    #     # yapf: disable
    #     stmt = (
    #         select(Route)
    #         .where(Route.is_active, Route.id.in_(ids))
    #         .options(
    #             load_only(
    #                 Route.id, Route.name, Route.description, Route.duration,
    #                 Route.rating, Route.created_at
    #             ),
    #             joinedload(Route.media)
    #         )
    #     )
    #     # yapf: enable
    #     return await self.fetch_all(stmt)
    #
    # async def query_in_radius(self,
    #                           params: MapQuery,
    #                           user: User,
    #                           tag_ids: list[Uid] | None = None) -> list[Route]:
    #     point = Point(params.longitude, params.latitude)
    #

    #     distance = Route.path.distance_centroid(point).label('distance')
    #
    #     stmt = select(Route).where(
    #         Route.is_active,
    #         Route.is_public,
    #         distance <= params.radius,
    #     )
    #     stmt = stmt.order_by(Route.rating.desc())
    #

    #     stmt = stmt.options(
    #         joinedload(Route.locations),
    #         joinedload(Route.saved_by.and_(User.id == user.id)).options(
    #             load_only(User.id)),
    #     )
    #     if tag_ids is not None:
    #         stmt = stmt.join(Route.route_tag_link).where(
    #             RouteTagLink.route_tag_id.in_(tag_ids))
    #

    #     stmt = stmt.offset(params.page_size * params.page)
    #
    #     return await self.fetch_all(stmt, limit=params.page_size)
    #
    # async def query_authored(self,
    #                          user: User,
    #                          page: Pagination,
    #                          public: bool = True) -> list[Route]:
    #     # yapf: disable
    #     stmt = (
    #         select(Route)
    #         .filter_by(user_id=user.id, is_public=public)
    #         .options(joinedload(Route.locations))
    #     )
    #     # yapf: enable
    #     return await self.fetch_all(stmt, limit=page)
    #
    # async def mark_saved(self, route: Route, user: User) -> None:
    #     user.saved_routes.add(route)
    #     await self.add_orm(user)
    #
    # async def delete_from_saved(self, route: Route, user: User) -> bool:
    #     if route not in user.saved_routes:
    #         return False
    #     user.saved_routes.remove(route)
    #     await self.add_orm(user)
    #     return True
    #
    # async def update(self, filters: Mapping, data: Mapping) -> Route | None:
    #     stmt = select(Route) \
    #         .filter_by(**filters).options(joinedload(Route.tags))
    #     route = await self.fetch_one(stmt)
    #     if not route:
    #         return None
    #
    #     tag_ids = data.get('tag_ids')
    #     if tag_ids is not None:
    #         stmt = select(RouteTag).where(RouteTag.id.in_(tag_ids))
    #         route.tags = set(await RouteTagDal(self.sess).fetch_all(stmt))
    #
    #     for attr, value in data.items():
    #         if attr == 'tag_ids':
    #             continue
    #         setattr(route, attr, value)
    #
    #     return await self.add_orm(route)
    #
    # async def mark_as_deleted(self, route: Route) -> Route:
    #     route.is_active = False
    #     return await self.add_orm(route)
    #
    # async def get_likers(self, route_id: Uid) -> list[User]:
    #     stmt = select(Route).filter_by(id=route_id).options(
    #         joinedload(Route.likers))
    #     r = await self.fetch_one(stmt)
    #     if r:
    #         return r.likers
    #     raise RouteNotFoundError