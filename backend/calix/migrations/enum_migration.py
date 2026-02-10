import logging

from alembic.autogenerate.api import AutogenContext
from alembic.autogenerate.compare import comparators
from alembic.operations.ops import AlterColumnOp
from sqlalchemy import Enum as SQLAEnum
from sqlalchemy.dialects.mysql import ENUM as MySQLEnum
from sqlalchemy.sql.schema import Column
from alembic.runtime.migration import log

logger: logging.Logger = logging.getLogger(log.name)


@comparators.dispatch_for("column")
def compare_column(
    autogen_context: AutogenContext,
    modify_ops: AlterColumnOp,
    schema: str | None,
    table_name: str,
    column_name: str,
    db_column: Column[MySQLEnum],
    model_column: Column[SQLAEnum],
) -> None:
    """Compare a column's model definition with its database state and modify the AlterColumnOp accordingly."""

    if isinstance(model_column.type, SQLAEnum) and isinstance(db_column.type, MySQLEnum):
        model_values: set[str] = set(model_column.type.enums)
        db_values: set[str] = set(db_column.type.enums)

        logger.debug(f"Comparing {table_name}.{column_name} db_values={db_values}, model_values={model_values}")

        if model_values ^ db_values:
            if new_values := model_values - db_values:
                logger.info(f"New values detected for Enum {table_name}.{column_name}: {', '.join(new_values)}")

            if removed_values := db_values - model_values:
                logger.info(f"Removed values detected for Enum {table_name}.{column_name}: {', '.join(removed_values)}")

            modify_ops.modify_type = model_column.type
            modify_ops.existing_type = SQLAEnum(*db_values, name=db_column.type.name or model_column.type.name)
            modify_ops.existing_nullable = db_column.nullable
