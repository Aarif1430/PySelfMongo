from unittest.mock import patch, MagicMock

from PySelfMongo import __version__
from PySelfMongo.py_self_mongo import PySelfMongo, MongoSingletonClient
import unittest


def test_version():
    assert __version__ == "0.1.0"


class MongoSingletonClientTest(unittest.TestCase):
    @patch("PySelfMongo.mongo.MongoClient")
    def test_singleton(self, mock_client):
        client = MongoSingletonClient()
        client.connect()
        mock_client.assert_called_once()
        new_client = MongoSingletonClient()
        new_client.connect()
        self.assertEqual(client, new_client)

    @patch("PySelfMongo.mongo.MongoClient")
    def test_singleton_with_args(self, mock_client):
        client = MongoSingletonClient(
            db_name="test_db", username="test_user", password="test_pass"
        )
        client.connect()
        mock_client.assert_called_once_with(
            "mongodb://test_user:test_pass@localhost:27017/test_db"
        )
        new_client = MongoSingletonClient(
            db_name="test_db", username="test_user", password="test_pass"
        )
        new_client.connect()
        self.assertEqual(client, new_client)

    @patch("PySelfMongo.mongo.MongoClient")
    def test_set_db_name(self, mock_client):
        client = MongoSingletonClient()
        client.set_db_name("test_db")
        client.connect()
        mock_client.assert_called_once_with(
            "mongodb://username:password@localhost:27017/db_name"
        )
        new_client = MongoSingletonClient()
        new_client.set_db_name("test_db")
        new_client.connect()
        self.assertEqual(client, new_client)
        self.assertEqual(client.db_name, new_client.db_name, "test_db")

    @patch("PySelfMongo.mongo.MongoClient")
    def test_set_username(self, mock_client):
        client = MongoSingletonClient()
        client.set_username("test_user")
        client.connect()
        mock_client.assert_called_once_with(
            "mongodb://username:password@localhost:27017/db_name"
        )
        new_client = MongoSingletonClient()
        new_client.set_username("test_user")
        new_client.connect()
        self.assertEqual(client, new_client)
        self.assertEqual(client.username, new_client.username, "test_user")

    @patch("PySelfMongo.mongo.MongoClient")
    def test_set_password(self, mock_client):
        client = MongoSingletonClient()
        client.set_password("test_pass")
        client.connect()
        mock_client.assert_called_once_with(
            "mongodb://username:password@localhost:27017/db_name"
        )
        new_client = MongoSingletonClient()
        new_client.set_password("test_pass")
        new_client.connect()
        self.assertEqual(client, new_client)
        self.assertEqual(client.password, new_client.password, "test_pass")
