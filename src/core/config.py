import os

from pydantic import BaseModel, PositiveInt


class MongoDBSettings(BaseModel):
    __MONGO_USER: str = os.getenv("MONGO_USER")
    __MONGO_PASSWORD: str = os.getenv("MONGO_PASSWORD")
    __MONGO_HOST: str = os.getenv("MONGO_HOST", "127.0.0.1")
    __MONGO_PORT: PositiveInt = int(os.getenv("MONGO_PORT", 27017))

    database_name: str = os.getenv("MONGO_DB_NAME", "user")
    url: str = (
        f"mongodb://{__MONGO_USER}:{__MONGO_PASSWORD}@{__MONGO_HOST}:{__MONGO_PORT}/"
    )


class Setting(BaseModel):
    api_v1_prefix: str = "/api/v1"
    mongodb: MongoDBSettings = MongoDBSettings()


settings = Setting()
