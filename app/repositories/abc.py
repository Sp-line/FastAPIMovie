from abc import ABC

from sqlalchemy.exc import IntegrityError

from schemas.db import IntegrityErrorData


class IntegrityCheckerABC(ABC):
    def _handle_integrity_error(self, exc: IntegrityError) -> None:
        pass

    @staticmethod
    def _get_integrity_error_data(exc: IntegrityError) -> IntegrityErrorData:
        cause = getattr(exc.orig, "__cause__", None)

        sqlstate = str(getattr(exc.orig, "sqlstate", ""))
        constraint = str(getattr(cause, "constraint_name", ""))
        table = str(getattr(cause, "table_name", ""))

        return IntegrityErrorData(
            sqlstate=sqlstate,
            constraint_name=constraint,
            table_name=table,
        )
