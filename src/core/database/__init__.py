from .db_helper import mongo_helper
from .mongo import AsyncMongoRegistryFactory

mongo_registry_factory = AsyncMongoRegistryFactory(mongo_helper.get_database())
WishlistsMongoRegistry = mongo_registry_factory.get_registry("wishlists")
