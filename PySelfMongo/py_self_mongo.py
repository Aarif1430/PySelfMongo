import logging
from pathlib import Path
from typing import Any, Dict, Generator, List, Optional

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.cursor import Cursor
from pymongo.database import Database
from yaml import safe_load


logger = logging.getLogger(__name__)


class MongoSingletonClient(object):
    """
    Singleton class for MongoClient.
    """

    __instance = None
    try:
        __config_file = Path(__file__).parent.parent / ".mongo_config.yaml"
        cfg = safe_load(open(__config_file, "r"))
        host = cfg["mongo"]["host"]
        port = cfg["mongo"]["port"]
        username = cfg["mongo"]["username"]
        password = cfg["mongo"]["password"]
        db_name = cfg["mongo"]["db_name"]
    except Exception as e:
        logger.error(
            f"Error while loading config file: {e}. Defaulting to localhost:27017"
        )
        host = "localhost"
        port = 27017

    @classmethod
    def __new__(cls, *args, **kwargs):
        if any(kwargs.values()):
            cls.set_db_name(kwargs["db_name"])
            cls.set_username(kwargs["username"])
            cls.set_password(kwargs["password"])
        if not cls.__instance:
            logger.info(f"Creating new instance of MongoClient")
            cls.__instance = MongoClient(
                f"mongodb://{cls.username}:{cls.password}@{cls.host}:{cls.port}/{cls.db_name}"
            )
        try:
            cls.__instance.server_info()
        except Exception as e:
            logger.error(f"Error while connecting to MongoDB: {e}")
            cls.__instance = MongoClient(
                f"mongodb://{cls.username}:{cls.password}@{cls.host}:{cls.port}/{cls.db_name}"
            )
        return cls.__instance[cls.db_name]

    @classmethod
    def set_db_name(cls, db_name: str):
        cls.db_name = db_name

    @classmethod
    def set_username(cls, username: str):
        cls.username = username

    @classmethod
    def set_password(cls, password: str):
        cls.password = password


class PySelfMongo(object):
    def __init__(
        self,
        user_name: Optional[str] = None,
        password: Optional[str] = None,
        database: Optional[str] = None,
    ):
        self.username = user_name
        self.password = password
        self.database = database

    def get_database_client(self) -> Database:
        """
        Get database from MongoDB.
        """
        return MongoSingletonClient(
            username=self.username, password=self.password, db_name=self.database
        )

    def get_collection(self, collection: str) -> Collection[Dict[str, Any]]:
        """
        :return:
        """
        return self.get_database_client()[collection]

    def get_document_by_id(self, collection: str, document_id: str) -> Dict[str, Any]:
        return self.get_collection(collection).find_one({"_id": document_id})

    def get_document_count(self, collection: str) -> int:
        return self.get_collection(collection).count_documents({})

    def get_document_by_field(
        self, collection: str, field: str, value: Any
    ) -> Cursor[dict[str, Any]]:
        return self.get_collection(collection).find({field: value})

    def get_document_by_query(self, collection: str, query: Dict[str, Any]) -> Cursor[dict[str, Any]]:
        return self.get_collection(collection).find(query)

    def get_document_by_query_with_projection(self, collection: str, query: Dict[str, Any], projection: Dict[str, Any]) -> Cursor[dict[str, Any]]:
        """
        Get document by query with projection.
        :param collection: Collection name.
        :param query: Query to find document.
        :param projection: Projection to get e.g {"_id": 0, "name": 1}
        :return:
        """
        return self.get_collection(collection).find(query, projection)

    def get_all_document_generators(
        self, collection: str, filters: List[Dict[str, Any]]
    ) -> Generator[Dict[str, Any], None, None]:
        """
        :param collection: Collection name
        :param filters: List of filters to apply to the query (e.g. [{"field": "value"}])
        :return: Generator of documents
        """
        for document in self.get_collection(collection).find({"$and": filters}):
            yield document

    def delete_document(self, collection: str, document_id: str) -> None:
        self.get_collection(collection).delete_one({"_id": document_id})

    def delete_document_by_field(self, collection: str, field: str, value: Any) -> None:
        self.get_collection(collection).delete_many({field: value})

    def delete_all_documents(self, collection: str) -> None:
        self.get_collection(collection).delete_many({})

    def insert_document(self, collection: str, document: Dict[str, Any]) -> None:
        self.get_collection(collection).insert_one(document)

    def insert_documents(
        self, collection: str, documents: List[Dict[str, Any]]
    ) -> None:
        self.get_collection(collection).insert_many(documents)

    def update_document(
        self, collection: str, document_id: str, document: Dict[str, Any]
    ) -> None:
        self.get_collection(collection).update_one(
            {"_id": document_id}, {"$set": document}
        )

    def update_document_by_field(
        self, collection: str, field: str, value: Any, document: Dict[str, Any]
    ) -> None:
        self.get_collection(collection).update_many({field: value}, {"$set": document})


if __name__ == "__main__":
    db_client = PySelfMongo()
    db = db_client.get_collection("transactions_dev")
