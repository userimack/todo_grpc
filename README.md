## Todo application using grpc, protobuf, sqlalchemy (alembic)


### Create a virtualenv and install dependencies
```
mkvirtualenv alembic_sample --python=/usr/local/bin/python3
pip install -r requirements.txt
```
Create a mysql database: `todo`

Configure `migrations/env.py` to update the `sqlalchemy.url` config if
the default config is different from your local setup.

### Running the migrations
```
alembic upgrade head
```

### To run grpc server
`python todo_server.py`

### To generate pb2 and pb2_grpc files
`python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. todo.proto`


### Connecting to grpc server from python terminal.

This is how clients connect to grpc and call rpc methods.
```
import grpc

import todo_pb2, todo_pb2_grpc


MAX_MESSAGE_LENGTH = 4 * 1024 * 1024 * 10
options = [
    ('grpc.max_send_message_length', MAX_MESSAGE_LENGTH),
    ('grpc.max_receive_message_length', MAX_MESSAGE_LENGTH)
]

channel = grpc.insecure_channel(
    'localhost:50051',
    options=options,
)
stub = todo_pb2_grpc.TodoServiceStub(channel)
```

### GetUsers
```
stub.GetUsers(todo_pb2.UsersRequest())
```

### GetUser
`stub.GetUser(todo_pb2.User(id=1))`

### GetUserTodos
`stub.GetUserTodos(todo_pb2.User(id=1))`

### GetTodo
```
stub.GetTodo(todo_pb2.Todo(id=3))
```

### CreateUser
```
user_req = todo_pb2.User(name="abc", email="ab@gmail.com")
user_resp = stub.CreateUser(user_req)

### CreateTodo
