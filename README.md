```
mkvirtualenv alembic_sample --python=/usr/local/bin/python3
pip install -r requirements.txt
```

create a mysql database: `learn_alembic`
Configure `alembic.ini` to update the `sqlalchemy.url` config.

### Create a new migration using alembic
```
alembic revision -m "create user table"
```

### Running the migration
```
# fill the upgrade and downgrade functions
alembic upgrade head
```

```
alembic current # will show the current migration
```

```
alembic revision -m "add age to users table"
```
### downgrading the migration
```
alembic downgrade <revision>

```

```
alembic revision -m "add address to users table"
```

```
# I can directly downgrade to first migration
```

```
# altering a column
```
```
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. todo.proto```
