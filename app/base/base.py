from abc import ABC, abstractmethod
from typing import Any, Iterable, Type

from psycopg2.extras import RealDictCursor
from pydantic import BaseModel

from .exceptions import NO_UPDATES_PROVIDED_EXCEPTION


class Base(ABC):
    def __init__(self, cursor: RealDictCursor):
        self._cursor = cursor


class BaseService(Base):
    @abstractmethod
    async def create(self, obj: Any) -> Any: ...

    @abstractmethod
    async def get_by_id(self, obj_id: int) -> Any: ...

    @abstractmethod
    async def get_all(self, page: int, page_size: int) -> list[Any]: ...

    @abstractmethod
    async def update_by_id(self, obj_id: int, obj_update: Any) -> Any: ...

    @abstractmethod
    async def delete_by_id(self, obj_id: int) -> None: ...


class BaseRepository(Base):

    def _excecute_query(
        self, query: str, variables: Iterable, commit: bool = True
    ) -> None:
        self._cursor.execute(query, variables)

        if commit:
            self._cursor.connection.commit()

    def _excecute_query_with_result(
        self,
        query: str,
        variables: Iterable,
        schema: Type[BaseModel],
        commit: bool = True,
    ) -> Any:
        self._cursor.execute(query, variables)

        if commit:
            self._cursor.connection.commit()

        if (res := self._cursor.fetchone()) is None:
            return None

        return schema.model_validate(dict(res))

    @abstractmethod
    def create(self, obj) -> Any: ...

    @abstractmethod
    def get_by_id(self, obj_id: int) -> Any: ...

    @abstractmethod
    def get_all(self, page: int, page_size: int) -> list[Any]: ...

    def _update_by_id(
        self,
        table_name: str,
        obj_id: int,
        obj_update: Any,
        schema: Type[BaseModel],
        id_field: str = "id",
    ) -> Any:
        query = f"UPDATE {table_name} SET "
        updates = []
        params = []

        for field, value in obj_update.model_dump(exclude_unset=True).items():
            updates.append(f"{field} = %s")
            params.append(value)

        if len(updates) == 0:
            raise NO_UPDATES_PROVIDED_EXCEPTION

        query += ", ".join(updates) + f" WHERE {id_field} = %s RETURNING *"
        params.append(obj_id)

        self._cursor.execute(query, params)
        self._cursor.connection.commit()

        if not (employee_record := self._cursor.fetchone()):
            return None

        return schema.model_validate(dict(employee_record))

    @abstractmethod
    def update_by_id(self, obj_id: int, obj_update: Any) -> Any: ...

    @abstractmethod
    def delete_by_id(self, obj_id: int) -> None: ...
