from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Final, Optional, ClassVar


class DataBase:

    _ENGINE: ClassVar[Optional[Engine]] = None
    _SESSIONMAKER: ClassVar[Optional[sessionmaker[Session]]] = None

    @classmethod
    def connect(cls, db_url: str) -> None:
        cls._ENGINE = create_engine(url=db_url)
        cls._SESSIONMAKER = sessionmaker(bind=cls._ENGINE)

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
