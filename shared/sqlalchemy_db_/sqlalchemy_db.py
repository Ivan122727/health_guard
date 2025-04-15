from functools import lru_cache

from shared.sqlalchemy_db_.database import SQLAlchemyDb

from shared.config import get_cached_settings
from shared.sqlalchemy_db_.sqlalchemy_model import SimpleDBM


def create_sqlalchemy_db() -> SQLAlchemyDb | None:
    if not get_cached_settings().database.DATABASE_URL and not get_cached_settings().database.ASYNC_DATABASE_URL:
        return None

    return SQLAlchemyDb(
        sync_db_url=get_cached_settings().database.DATABASE_URL,
        async_db_url=get_cached_settings().database.ASYNC_DATABASE_URL,
        base_dbm=SimpleDBM
    )


@lru_cache()
def get_cached_sqlalchemy_db() -> SQLAlchemyDb | None:
    return create_sqlalchemy_db()