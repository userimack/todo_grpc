from concurrent import futures
import time
import logging
import sys
from functools import wraps

import grpc

import todo_pb2
from todo_pb2 import User as User_pb2, UsersList, TodosList
import todo_pb2_grpc
from models import session, User, Todo

log_format = '%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s'
logging.basicConfig(
    stream=sys.stdout, level=logging.DEBUG,
    format=log_format, datefmt="%Y-%m-%d %H:%M:%S"
)


def log_request(function):
    @wraps(function)
    def inner_function(*args, **kwargs):
        logging.info("received request: {}".format(function.__name__))
        resp = function(*args, **kwargs)
        return resp
    return inner_function


class TodoService(todo_pb2_grpc.TodoServiceServicer):

    @log_request
    def GetUsers(self, request, context):
        users = session.query(User).all()
        userslist_pb = []
        for user in users:
            userslist_pb.append(
                todo_pb2.User(
                    id=user.id,
                    name=user.name,
                    email=user.email
                )
            )
        return todo_pb2.UsersList(users=userslist_pb)

    @log_request
    def GetUser(self, request, context):
        user_id = request.id
        user = session.query(User).filter(User.id == user_id).first()
        user_pb2 = todo_pb2.User()

        if user:
            user_pb2.id = user.id
            user_pb2.name = user.name
            user_pb2.email = user.email

        return user_pb2

    @log_request
    def GetUserTodos(self, request, context):
        user_id = request.id
        user = session.query(User).filter(User.id == user_id).first()
        if user:
            todos = user.todos
            todos_pb2 = []
            for todo in todos:
                todos_pb2.append(todo_pb2.Todo(**self._row2dict(todo)))
        else:
            return todo_pb2.TodosList()

        return TodosList(todos=todos_pb2)

    @log_request
    def GetTodo(self, request, context):
        todo_id = request.id
        todo = session.query(Todo).filter(Todo.id == todo_id).first()
        if todo:
            return todo_pb2.Todo(**self._row2dict(todo))
        else:
            return todo_pb2.Todo()

    @log_request
    def CreateUser(self, request, context):
        user = User(name=request.name, email=request.name)
        try:
            session.add(user)
            session.commit()
        except:
            logging.error("Didn't create user")
        finally:
            # if success returns with id else the request user sent
            return todo_pb2.User(**self._row2dict(user))

    @log_request
    def CreateTodo(self, request, context):
        todo = Todo(text=request.text, user_id=request.user_id, state=request.state)
        try:
            session.add(todo)
            session.commit()
        except:
            logging.error("Didn't create todo")
        finally:
            # if success returns with id else the request user sent
            return todo_pb2.User(**self._row2dict(todo))

    def _row2dict(self, row):
        row_dict = {}
        for col in row.__table__.columns.keys():
            row_dict[col] = getattr(row, col)

        return row_dict


if __name__ == '__main__':
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    todo_pb2_grpc.add_TodoServiceServicer_to_server(TodoService(), server)

    server.add_insecure_port('0.0.0.0:50051')
    server.start()
    print("TODO grpc server started")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)
