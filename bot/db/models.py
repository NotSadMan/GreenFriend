from datetime import datetime

from sqlalchemy import BIGINT, VARCHAR, BOOLEAN, UniqueConstraint, INTEGER, ForeignKey, DateTime
from sqlalchemy.orm import mapped_column, Mapped

from bot.db.base import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint(
            'user_id',
            name='unique_users_user_id'
        ),
    )

    user_id: Mapped[int] = mapped_column(BIGINT, nullable=False, primary_key=True)
    username: Mapped[str] = mapped_column(VARCHAR(length=32), nullable=True)
    ban: Mapped[bool] = mapped_column(BOOLEAN, default=False, nullable=False)


class Plant(Base):
    __tablename__ = "plants"

    plant_id: Mapped[int] = mapped_column(INTEGER, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BIGINT, ForeignKey('users.user_id'), nullable=False)
    plant_name: Mapped[str] = mapped_column(VARCHAR(length=64), nullable=False)
    plant_photo: Mapped[str] = mapped_column(VARCHAR(length=256), nullable=True)
    watering_frequency: Mapped[int] = mapped_column(INTEGER, nullable=False)
    last_watered: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    notifications_enabled: Mapped[bool] = mapped_column(BOOLEAN, default=False)



