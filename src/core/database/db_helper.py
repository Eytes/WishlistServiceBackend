from typing import AsyncGenerator

from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorClientSession,
    AsyncIOMotorDatabase,
)

from ..config import settings


class AsyncMongoDBHelper:
    """
    Класс для работы с MongoDB с использованием асинхронных операций и сессий.

    Этот класс инкапсулирует подключение к MongoDB и управление сессиями для обеспечения атомарности операций.
    """

    def __init__(self, client_url: str, database_name: str) -> None:
        """
        Инициализация клиента MongoDB и базы данных.

        :param client_url: URL для подключения к MongoDB.
        :param database_name: Название базы данных, с которой будет работать данный класс.
        """
        self.__mongo_client = AsyncIOMotorClient(
            client_url,
            uuidRepresentation="standard",
        )
        self.__mongo_database = self.__mongo_client[database_name]

    def get_database(self) -> AsyncIOMotorDatabase:
        """
        Получить доступ к базе данных MongoDB.

        :return: Экземпляр базы данных MongoDB, с которой будет работать данный класс.
        """
        return self.__mongo_database

    async def get_session(self) -> AsyncGenerator[AsyncIOMotorClientSession, None]:
        """
        Создать новую сессию для выполнения операций в рамках одной транзакции.

        Сессия будет автоматически завершена после окончания операций.

        :return: Генератор, который при итерировании возвращает сессию MongoDB.
        """
        async with await self.__mongo_client.start_session() as session:
            yield session
            await session.end_session()


# Экземпляр помощника для работы с MongoDB.
mongo_helper = AsyncMongoDBHelper(
    client_url=settings.mongodb.url,
    database_name=settings.mongodb.database_name,
)
