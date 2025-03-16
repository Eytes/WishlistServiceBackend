import os

from pydantic import BaseModel, PositiveInt
from pydantic_settings import BaseSettings


class MongoDBSettings(BaseSettings):
    MONGO_USER: str
    MONGO_PASSWORD: str
    MONGO_HOST: str
    MONGO_PORT: PositiveInt = 27017
    DATABASE_NAME: str = "Wishlists"

    url: str = (
        f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/"
    )


class Setting(BaseSettings):
    api_v1_prefix: str = "/api/v1"
    mongodb: MongoDBSettings = MongoDBSettings()


settings = Setting()
