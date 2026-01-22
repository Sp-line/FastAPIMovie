from typing import Any

from pydantic import BaseModel


class DBException(Exception):
    pass


class ObjectException(DBException):
    pass


class ObjectNotFoundException(ObjectException):
    def __init__(self, obj_id: Any, table_name: str) -> None:
        self.table_name = table_name
        self.obj_id = obj_id

        if isinstance(obj_id, BaseModel):
            id_repr = ", ".join([f"{k}={v}" for k, v in obj_id.model_dump().items()])
            id_repr = f"({id_repr})"
        else:
            id_repr = str(obj_id)

        super().__init__(f"Object with id {id_repr} not found in table '{table_name}'")


class UniqueFieldException(DBException):
    def __init__(self, field_name: str, table_name: str) -> None:
        self.field_name = field_name
        self.table_name = table_name

        super().__init__(f"This '{field_name}' already exists in table '{table_name}'")


class UniqueException(DBException):
    def __init__(self, table_name: str, *fields: str) -> None:
        self.table_name = table_name
        self.fields = fields

        fields_str = ', '.join(fields)
        super().__init__(f"Object with fields '{fields_str}' already exists in table '{table_name}'")


class RelatedObjectNotFoundException(ObjectException):
    def __init__(self, field_name: str, table_name: str) -> None:
        self.field_name = field_name
        self.table_name = table_name

        super().__init__(f"Related object not found for field '{field_name}' in table '{table_name}'")


class DeleteConstraintException(DBException):
    def __init__(self, table_name: str, referencing_table: str) -> None:
        self.table_name = table_name
        self.referencing_table = referencing_table

        super().__init__(
            f"Cannot delete object from table '{table_name}' because it is referenced by existing records in table '{referencing_table}'"
        )
