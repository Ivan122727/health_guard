import sqlalchemy
import pytz
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column
from shared.sqlalchemy_db_.database import BaseDBM


class SimpleDBM(BaseDBM):
    __abstract__ = True

    id: Mapped[int] = mapped_column(
        sqlalchemy.BIGINT,
        nullable=False,
        primary_key=True,
        autoincrement=True,
        sort_order=-103,
    )
    
    creation_dt: Mapped[datetime] = mapped_column(
        sqlalchemy.TIMESTAMP(timezone=True),
        nullable=False,
        index=True,
        insert_default=datetime.now(tz=pytz.UTC),
        server_default=func.now(),
        sort_order=-100,
    )

    def __repr__(self) -> str:
        parts = [f"id={self.id}"]
        return f"{self.entity_name} ({', '.join(parts)})"

    @property
    def entity_name(self) -> str:
        return self.__class__.__name__.removesuffix("DBM")

    @property
    def sdp_entity_name(self) -> str:
        return self.entity_name


def get_simple_dbm_class() -> type[SimpleDBM]:
    from shared.sqlalchemy_db_.sqlalchemy_model import SimpleDBM
    return SimpleDBM

