from sqlalchemy import select
from sqlalchemy.orm import joinedload

from src.dal.dal import Dal
from src.db.models.tables import Patient, Relative, Relationship, Document
from src.schemas.document import DocumentIn
from src.schemas.patient import PatientIn, PatientUpdate
from src.schemas.relative import RelativeIn
from src.utils.errors import ItemNotFoundError


class PatientDal(Dal[Patient]):
    model = Patient

    def get_patients(self) -> list[Patient] | None:
        filters = select(self.model)
        return self.fetch_all(filters)

    def get_patient_by_id(self, patient_id: int, options = None) -> Patient:
        patient = self.get_(patient_id, options=options)
        if patient is None:
            raise ItemNotFoundError

        return patient

    def create(self, schema: PatientIn) -> Patient:
        patient = Patient(**schema.dict())
        return self.add_orm(patient)

    #
    def update_patient_by_id(self, patient_id: int, data: PatientUpdate) -> Patient:
        filters = {'id': patient_id}
        patch = data.dict(exclude_unset=True)
        updated_patient = self.update(filters, patch)
        if updated_patient is None:
            raise ItemNotFoundError  # Посмотреть что должно возвращаться по соглашению
        return self.update(filters, patch)

    def delete_by_id(self, patient_id: int) -> None:
        patient = self.get_patient_by_id(patient_id, options=[
            joinedload(Patient.relatives)
        ])
        for relative in patient.relatives:
            if len(relative.patients) == 1:
                 self.delete_orm(relative)
        self.sess.flush()
        self.delete_orm(patient)


        # if patient is None:
        #     raise ItemNotFoundError
        #
        # self.delete_orm(patient)
        #
        # for relative in patient.relatives:
        #     if len(relative.patients) == 1:
        #         self.delete_orm(relative)

        return None

    def create_relative(self, patient_id: int, relative_data: RelativeIn) -> (Relative, Relationship):
        patient = self.get_patient_by_id(patient_id)
        relation = Relationship(**relative_data.dict(include={"relationship_type"}))
        relative = Relative(**relative_data.dict(exclude={"relationship_type"}))
        relation.relative = relative
        patient.relative_association.append(relation)
        self.sess.flush()
        self.sess.refresh(relative)
        self.sess.refresh(relation)
        return relative, relation

    def get_patient_w_relationship_a_relative(self, patient_id: int) -> Patient:
        patient = self.get_patient_by_id(patient_id, options=[
            joinedload(Patient.relative_association).joinedload(Relationship.relative)])

        return patient


    def create_document(self, patient_id: int, document_data: DocumentIn) -> Document:
        patient = self.get_patient_by_id(patient_id)
        document = Document(**document_data.dict())
        patient.documents.append(document)
        self.sess.flush()
        self.sess.refresh(document)
        return document

    def get_patient_documents(self, patient_id: int) -> list[Document]:
        patient = self.get_patient_by_id(patient_id, options=[joinedload(Patient.documents)])
        print(patient.documents)
        return patient.documents




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
