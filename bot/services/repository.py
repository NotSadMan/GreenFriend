from sqlalchemy import select, func
import datetime

from bot.db.models import User, Plant


class Repo:
    """
    Репозиторий для работы с базой данных.

    Args:
        session: Сессия SQLAlchemy.
    """

    def __init__(self, session):
        self.session = session

    async def add_user(self, user_id: int, username: str) -> bool:
        statement = select(User).where(User.user_id == user_id)
        new_user = True if await self.session.scalar(statement) is None else False
        if new_user:
            new_user_add = User(
                user_id=user_id,
                username=username
            )
            self.session.add(new_user_add)
            await self.session.commit()
            return True
        return False

    async def get_users(self) -> list[int]:
        """
        Возвращает список ID всех пользователей.

        Returns:
            Список ID пользователей.
        """
        statement = select(User.user_id)
        users = await self.session.scalars(statement)
        return users.all()

    async def get_user(self, user_id: int) -> User | None:
        """
        Возвращает пользователя по его ID.

        Args:
            user_id: ID пользователя.

        Returns:
            Объект User, если пользователь найден, None в противном случае.
        """
        return await self.session.get(User, user_id)

    async def get_user_count(self) -> int:
        """
        Возвращает количество пользователей в базе данных.

        Returns:
            Количество пользователей.
        """
        return await self.session.scalar(select(func.count()).select_from(User))

    async def change_ban_status(self, user_id: int, ban_status: int) -> None:
        """
        Изменяет статус блокировки пользователя.

        Args:
            user_id: ID пользователя.
            ban_status: Новый статус блокировки.
        """
        user = await self.session.get(User, user_id)
        if user:
            user.ban = ban_status
            await self.session.commit()

    async def add_plant(self, user_id: int, name: str, photo: str, watering_frequency: int) -> None:
        """
        Добавляет новое растение в базу данных.

        Args:
            user_id: ID пользователя, добавившего растение.
            name: Название растения.
            photo: Фото растения.
            watering_frequency: Частота полива (в днях).
        """
        new_plant = Plant(
            user_id=user_id,
            plant_name=name,
            plant_photo=photo,
            watering_frequency=watering_frequency,
            last_watered=datetime.datetime.now(),
        )
        self.session.add(new_plant)
        await self.session.commit()

    async def get_plant(self, plant_id: int) -> Plant | None:
        """
        Возвращает растение по его ID.

        Args:
            plant_id: ID растения.

        Returns:
            Объект Plant, если растение найдено, None в противном случае.
        """
        return await self.session.get(Plant, plant_id)

    async def get_plants(self, user_id: int) -> list[Plant]:
        """
        Возвращает список растений пользователя.

        Args:
            user_id: ID пользователя.

        Returns:
            Список объектов Plant.
        """
        statement = select(Plant).where(Plant.user_id == user_id)
        plants = await self.session.scalars(statement)
        return plants.all()

    async def change_notifications(self, plant_id: int, notifications_enabled: bool) -> bool:
        """
        Изменяет состояние уведомлений для растения.

        Args:
            plant_id: ID растения.
            notifications_enabled: Новое состояние уведомлений.

        Returns:
            Новое состояние уведомлений.
        """
        plant = await self.session.get(Plant, plant_id)
        if plant:
            plant.notifications_enabled = notifications_enabled
            await self.session.commit()
            return notifications_enabled
        return False

    async def delete_plant(self, plant_id: int) -> None:
        """
        Удаляет растение из базы данных.

        Args:
            plant_id: ID растения.
        """
        plant = await self.session.get(Plant, plant_id)
        if plant:
            await self.session.delete(plant)
            await self.session.commit()