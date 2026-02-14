from sqlalchemy.exc import IntegrityError

from schemas.db import ConstraintRule, IntegrityErrorData


class TableErrorHandler:
    def __init__(self, *constraints: ConstraintRule) -> None:
        self._rules_map = {
            (rule.error_code.value, rule.name): rule
            for rule in constraints
        }

    @staticmethod
    def _parse_integrity_error(exc: IntegrityError) -> IntegrityErrorData:
        cause = getattr(exc.orig, "__cause__", None)

        sqlstate = str(getattr(exc.orig, "sqlstate", ""))
        constraint = str(getattr(cause, "constraint_name", ""))
        table = str(getattr(cause, "table_name", ""))

        return IntegrityErrorData(
            sqlstate=sqlstate,
            constraint_name=constraint,
            table_name=table,
        )

    def handle(self, exc: IntegrityError) -> None:
        error_data = self._parse_integrity_error(exc)
        key = (error_data.sqlstate, error_data.constraint_name)
        rule = self._rules_map.get(key)

        if rule:
            raise rule.exception from exc
