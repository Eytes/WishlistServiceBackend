from typing import Any, Generic, TypeVar

from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorDatabase

T = TypeVar("T")


class AsyncMongoRegistry(Generic[T]):
    """
    Класс для работы с коллекцией MongoDB с использованием асинхронных операций.

    Этот класс инкапсулирует основные операции с коллекцией MongoDB, такие как создание, получение, обновление и удаление записей.
    """

    def __init__(self, collection: AsyncIOMotorCollection) -> None:
        """
        Инициализация реестра для работы с коллекцией MongoDB.

        :param collection: Коллекция MongoDB, с которой будет работать данный реестр.
        """
        self.__collection = collection

    async def get(self, item_id: T) -> dict[str, Any] | None:
        """
        Получить запись из коллекции MongoDB по ID.

        :param item_id: Уникальный идентификатор записи в коллекции.
        :return: Запись из коллекции в виде словаря, либо None, если запись не найдена.
        """
        return await self.__collection.find_one({"_id": item_id})

    async def create(self, item_data: T) -> Any:
        """
        Создание новой записи в коллекции MongoDB.

        :param item_data: Модель данных, которая будет сериализована и вставлена в коллекцию.
        :return: ID новой записи, которая была вставлена в коллекцию.
        """
        result = await self.__collection.insert_one(item_data.model_dump(by_alias=True))
        return result.inserted_id

    async def delete(self, item_id: T) -> None:
        """
        Удалить запись из коллекции MongoDB по ID.

        :param item_id: Уникальный идентификатор записи, которую нужно удалить.
        :return: None
        """
        await self.__collection.find_one_and_delete({"_id": item_id})

    async def update(self, item_id: T, new_data: dict) -> dict[str, Any] | None:
        """
        Обновление записи в коллекции MongoDB по ID.

        Этот метод находит запись по переданному ID и обновляет её с использованием новых данных.

        :param item_id: Уникальный идентификатор записи, которую нужно обновить.
                         Тип ID зависит от структуры данных в базе данных (например, строка или ObjectId).
        :param new_data: Новый набор данных для обновления записи. Должен быть в виде словаря,
                         где ключи — это поля, которые будут обновлены, а значения — новые данные для этих полей.
        :return: Обновлённая запись в виде словаря, если обновление было успешным, или None,
                 если запись с таким ID не найдена или не было обновлений.
        """
        return await self.__collection.find_one_and_update(
            filter={"_id": item_id},
            update={"$set": new_data},
            return_document=True,
        )


class AsyncMongoRegistryFactory:
    """
    Фабрика для создания экземпляров `AsyncMongoRegistry` для разных коллекций.

    Этот класс предоставляет интерфейс для создания экземпляров `AsyncMongoRegistry`
    для работы с различными коллекциями в базе данных MongoDB.
    """

    def __init__(self, database: AsyncIOMotorDatabase):
        """
        Инициализация фабрики для создания реестров для коллекций.

        :param database: База данных MongoDB, с которой будет работать фабрика.
        """
        self.__database = database

    def get_registry(self, collection_name: str) -> AsyncMongoRegistry:
        """
        Получить реестр для работы с конкретной коллекцией.

        :param collection_name: Название коллекции MongoDB, с которой необходимо работать.
        :return: Экземпляр `AsyncMongoRegistry`, настроенный для работы с указанной коллекцией.
        """
        return AsyncMongoRegistry(self.__database[collection_name])
