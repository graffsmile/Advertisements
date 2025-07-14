import datetime
from sqlalchemy import Boolean, String, Integer, DateTime, func, ForeignKey
from sqlalchemy.ext.asyncio import (AsyncAttrs, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

import config

engine = create_async_engine(config.POSTGRES_DSN)
Session = async_sessionmaker(bind=engine, expire_on_commit=False)

class Base(DeclarativeBase, AsyncAttrs):

    @property
    def id_dict(self):
        return {"id": self.id}

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    registration_time: Mapped[datetime.datetime] = mapped_column(
        DateTime, server_default=func.now()
    )

    adverts = relationship(
        "Adverts",
        back_populates="author",
        cascade="all, delete",
        passive_deletes=True,
        lazy="joined",
    )

    @property
    def dict(self):

        return {
            "id": self.id,
            "name": self.name,
            "registration_time": self.registration_time.isoformat(),
        }


class Adverts(Base):
    __tablename__ = "adverts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    description: Mapped[str] = mapped_column(String(1000), nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=True)
    creation_time: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    author_id: Mapped[User] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    author = relationship(
        "User",
        back_populates="adverts",
        lazy="joined",
    )

    @property
    def dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "creation_time": self.creation_time.isoformat(),
            "author_id": self.author_id,
            "author_name": self.author.name
        }


USER_OBJ = User
USER_CLS = type(User)
ADVERT_OBJ = Adverts
ADVERT_CLS = type(Adverts)

async def init_orm():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_orm():
    await engine.dispose()