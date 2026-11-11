import atexit
import datetime
import os

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    scoped_session,
    sessionmaker,
)

POSTGRES_DB = os.getenv("POSTGRES_DB", "app")
POSTGRES_USER = os.getenv("POSTGRES_USER", "app")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "secret-password")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5431")

POSTGRES_DSN = (
    f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
    f"{POSTGRES_HOST}:{POSTGRES_PORT}/"
    f"{POSTGRES_DB}"
)

engine = create_engine(POSTGRES_DSN)
atexit.register(engine.dispose)

Session = sessionmaker(bind=engine)
db_session = scoped_session(Session)


class Base(DeclarativeBase):
    pass


# 1. Модель пользователя
class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String)
    registration_time: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
    )
    postings: Mapped[list["Posting"]] = relationship(
        "Posting",
        back_populates="owner_obj",
        cascade="all, delete, delete-orphan",
        passive_deletes=True,
    )

    @property
    def user_dict(self) -> dict:
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "registration_time": int(self.registration_time.timestamp()),
            # 'postings':[p.posting_heading_dict for p in self.postings]
        }


# 2. Модель объявления (Posting)
class Posting(Base):
    __tablename__ = "postings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    heading: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    registration_time: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
    )
    # Внешний ключ, связывающий объявление с пользователем (owner_id в БД)
    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False, index=True
    )
    # ORM-объект владельца
    owner_obj: Mapped[User] = relationship("User", back_populates="postings")

    @property
    def id_dict(self):
        return {"id": self.id}

    @property
    def posting_dict(self):
        return {
            "id": self.id,
            "heading": self.heading,
            "description": self.description,
            "registration_time": int(self.registration_time.timestamp()),
            "owner_id": self.owner_id,
            "owner": self.owner_obj.user_dict,
        }

    @property
    def posting_heading_dict(self):
        return {
            "id": self.id,
            "heading": self.heading,
        }


Base.metadata.create_all(bind=engine)
