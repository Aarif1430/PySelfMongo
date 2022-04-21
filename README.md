Py Self Mongo
==========

A self mongo client for the [MongoDB][mongo] database is a thin client that connects to a mongo server and provides a simple interface to the database.
A client is written as a singleton to make sure that only one connection is open at a time. The connection timeout is taken care by checking the server info every time a request is made.
A new connection is made if the server info is not available or the connection has timed out. The project is developed using poetry and the [Pytest][pytest] framework.

How to use
----------
1. Create a config file with name `.mongo_config.yaml` in the root directory of the project. The config file should contain the following fields:

```yaml
mongo:
  host:
    localhost
  port:
    27017
  db_name:
    db_name
  password:
    password
  username:
    username
```
The host can be an IP address or a hostname. E.g. In case of a hosted mongo server in aws, the hostname is `ec2-*-**-**-**.**-east-2.compute.amazonaws.com`.
The client can be used as follows:

```python
from py_self_mongo import PySelfMongo

mongo_client = PySelfMongo()
mongo_client.get_collection('collection_name')
```

2. If no config file is found, the client will try to connect to the localhost with default port 27017. In this case the client can be intialized as follows:

```python
from py_self_mongo import PySelfMongo

mongo_client = PySelfMongo(db_name='db_name', username='user_name', password='password')
mongo_client.get_collection('collection_name')
```

Methods and attributes
---------------------
- `get_collection(collection_name)`: Returns a collection object.
- `get_document_by_id(collection_name, document_id)`: Returns a document object.
- `get_document_by_query(collection_name, query)`: Returns a list of document objects.
- `get_document_by_query_with_projection(collection_name, query, projection)`: Returns a list of document objects.
- `get_all_document_generatosr(collection_name, filter)`: Returns a generator of all documents in the collection.
- `delete_document(collection_name, document_id)`: Deletes a document.
- `delete_document_by_id(collection_name, document_id)`: Deletes a document.
- `update_document_by_field(collection_name, field, value)`: Updates a document

Installation
------------
Install using pip:
```bash
$ pip install py_self_mongo
```

