from datetime import datetime, timedelta
import logging
from typing import Any, Collection
import pytz
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import create_engine, QueuePool, inspect, AsyncAdaptedQueuePool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm.session import Session


class BaseDBM(DeclarativeBase):
    __abstract__ = True
    __table_args__ = {"extend_existing": True}

    _bus_data: dict[str, Any] | None = None

    @property
    def bus_data(self) -> dict[str, Any]:
        if self._bus_data is None:
            self._bus_data = {}
        return self._bus_data

    def simple_dict(
            self,
            *,
            need_include_columns: bool = True,
            need_include_sd_properties: bool = True,
            include_columns: Collection[str] | None = None,
            exclude_columns: Collection[str] | None = None,
            include_sd_properties: Collection[str] | None = None,
            exclude_sd_properties: Collection[str] | None = None,
            include_columns_and_sd_properties: Collection[str] | None = None,
            kwargs: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        if exclude_columns is None:
            exclude_columns = set()
        if exclude_sd_properties is None:
            exclude_sd_properties = set()

        res = {}

        if need_include_columns:
            for c in inspect(self).mapper.column_attrs:
                if include_columns_and_sd_properties is not None and c.key not in include_columns_and_sd_properties:
                    continue
                if include_columns is not None and c.key not in include_columns:
                    continue
                if c.key in exclude_columns:
                    continue
                value = getattr(self, c.key)
                res[c.key] = value

        if need_include_sd_properties:
            for attr_name in dir(self):
                if not attr_name.startswith("sdp_") or not isinstance(getattr(type(self), attr_name, None), property):
                    continue

                sd_property_name = attr_name.removeprefix("sdp_")

                if (
                        include_columns_and_sd_properties is not None
                        and sd_property_name not in include_columns_and_sd_properties
                ):
                    continue
                if include_sd_properties is not None and sd_property_name not in include_sd_properties:
                    continue
                if sd_property_name in exclude_sd_properties:
                    continue

                res[sd_property_name] = getattr(self, attr_name)

        if kwargs is not None:
            res.update(kwargs)

        return res


class SQLAlchemyDb:
    def __init__(
            self,
            *,
            sync_db_url: str | None,
            async_db_url: str | None,
            db_echo: bool = False,
            base_dbm: type[BaseDBM] | None = None,
            db_models: list[Any] | None = None,
    ):
        self._logger = logging.getLogger(self.__class__.__name__)

        self.db_url = sync_db_url
        if self.db_url is not None:
            self.engine = create_engine(
                url=sync_db_url,
                echo=db_echo,
                pool_size=10,
                max_overflow=10,
                poolclass=QueuePool,
                pool_timeout=timedelta(seconds=30).total_seconds(),
            )
        self.sessionmaker = sessionmaker(bind=self.engine)
        self.func_new_session_counter = 0

        self.async_db_url = async_db_url
        if self.async_db_url is not None:
            self.async_engine = create_async_engine(
                url=async_db_url,
                echo=db_echo,
                pool_size=10,
                max_overflow=10,
                poolclass=AsyncAdaptedQueuePool,
                pool_timeout=timedelta(seconds=30).total_seconds()
            )
        self.async_sessionmaker = async_sessionmaker(bind=self.async_engine)
        self.func_new_async_session_counter = 0

        self.base_dbm = base_dbm
        self.db_models = db_models

    def init(self):
        self.base_dbm.metadata.create_all(bind=self.engine, checkfirst=True)
        self._logger.info("inited")
    
    def drop(self):
        self.base_dbm.metadata.drop_all(bind=self.engine, checkfirst=True)
        self._logger.info("dropped")

    def reinit(self):
        self.base_dbm.metadata.drop_all(bind=self.engine, checkfirst=True)
        self.base_dbm.metadata.create_all(bind=self.engine, checkfirst=True)
        self._logger.info("reinited")

    def check_conn(self):
        self.engine.connect()
        self._logger.info("db conn is good")

    def new_session(self, **kwargs) -> Session:
        self.func_new_session_counter += 1
        return self.sessionmaker(**kwargs)
    
    
    def new_async_session(self, **kwargs) -> AsyncSession:
        self.func_new_async_session_counter += 1
        return self.async_sessionmaker(**kwargs)
    
    def is_conn_good(self) -> bool:
        try:
            self.check_conn()
        except Exception as e:
            self._logger.error(e)
            return False
        return True
    
    def generate_creation_dt(self) -> datetime:
        return datetime.now(tz=pytz.UTC)