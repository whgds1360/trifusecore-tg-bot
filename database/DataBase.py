from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm.decl_api import DeclarativeMeta

from typing import Optional, ClassVar


class DataBase:

    _ENGINE: ClassVar[Optional[Engine]] = None
    _SESSIONMAKER: ClassVar[Optional[sessionmaker[Session]]] = None
    _USERS: ClassVar[Optional[DeclarativeMeta]] = None

    @classmethod
    def connect(cls, db_url: str) -> None:
        cls._ENGINE = create_engine(url=db_url)
        cls._SESSIONMAKER = sessionmaker(bind=cls._ENGINE)

        base = automap_base()
        base.prepare(autoload_with=cls._ENGINE)

        cls._USERS = base.classes.users

    @classmethod
    def get_engine(cls) -> Engine:
        if cls._ENGINE is None:
            raise RuntimeError("База данных не подключена!")
        return cls._ENGINE

    @classmethod
    def get_sessionmaker(cls) -> sessionmaker[Session]:
        if cls._SESSIONMAKER is None:
            raise RuntimeError("База данных не подключена. Вызовите connect()")
        return cls._SESSIONMAKER

    @classmethod
    def get_users(cls) -> DeclarativeMeta:
        if cls._USERS is None:
            raise RuntimeError("База данных не подключена. Вызовите connect()")
        return cls._USERS
