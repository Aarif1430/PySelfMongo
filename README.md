Self Mongo
==========

A self mongo client for the [MongoDB][mongo] database is a thin client that connects to a mongo server and provides a simple interface to the database.
A client is written as a singleton to make sure that only one connection is open at a time. The connection timeout is taken care by checking the server info every time a request is made.
A new connection is made if the server info is not available or the connection has timed out.

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
from self_mongo import SelfMongo
mongo_client = SelfMongo()
mongo_client.get_collection('collection_name')
```

2. If no config file is found, the client will try to connect to the localhost with default port 27017. In this case the client can be intialized as follows:

```python
from self_mongo import SelfMongo
mongo_client = SelfMongo(db_name='db_name', username='user_name', password='password')
mongo_client.get_collection('collection_name')
```

Methods and attributes
---------------------
- `get_collection(collection_name)`: Returns a collection object.
- `get_db()`: Returns the database object.
- `get_server_info()`: Returns the server info.
- `get_db_name()`: Returns the database name.
- `get_host()`: Returns the host.
- `get_port()`: Returns the port.
- `get_username()`: Returns the username.
- `get_password()`: Returns the password.
- `get_connection_timeout()`: Returns the connection timeout.
- `set_connection_timeout(timeout)`: Sets the connection timeout.
- `set_db_name(db_name)`: Sets the database name.
- `set_host(host)`: Sets the host.
- `set_port(port)`: Sets the port.