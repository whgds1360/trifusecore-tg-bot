from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm.decl_api import DeclarativeMeta

from typing import Optional, ClassVar, final


@final
class DataBase:
    """Управляет подключением к базе данных и предоставляет доступ к моделям."""

    # Движок SQLAlchemy для подключения к БД
    _ENGINE: ClassVar[Optional[Engine]] = None

    # Фабрика сессий для работы с БД
    _SESSIONMAKER: ClassVar[Optional[sessionmaker[Session]]] = None

    # Модель таблицы users из БД
    _USERS: ClassVar[Optional[DeclarativeMeta]] = None

    @classmethod
    def connect(cls, db_url: str) -> None:
        """Подключается к базе данных и создает ORM-модель."""
        cls._ENGINE = create_engine(url=db_url)
        cls._SESSIONMAKER = sessionmaker(bind=cls._ENGINE)

        base = automap_base()  # Автоматический создает модель из сущ-ей бд.
        base.prepare(autoload_with=cls._ENGINE)

        cls._USERS = base.classes.users

    @classmethod
    def get_engine(cls) -> Engine:
        """Возвращает движок базы."""
        if cls._ENGINE is None:
            raise RuntimeError("База данных не подключена. Вызовите connect()")
        return cls._ENGINE

    @classmethod
    def get_sessionmaker(cls) -> sessionmaker[Session]:
        """Возвращает фабрику для создания сессий."""
        if cls._SESSIONMAKER is None:
            raise RuntimeError("База данных не подключена. Вызовите connect()")
        return cls._SESSIONMAKER

    @classmethod
    def get_users(cls) -> DeclarativeMeta:
        """Возвращает ORM-модель для работы с таблицей users."""
        if cls._USERS is None:
            raise RuntimeError("База данных не подключена. Вызовите connect()")
        return cls._USERS
