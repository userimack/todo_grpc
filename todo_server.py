from concurrent import futures
import time
import logging
import sys

import grpc

from todo_pb2 import Todo as Todo_pb2, User as User_pb2, UsersList, TodosList
import todo_pb2_grpc
from models import session, User, Todo

log_format = '%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s'
logging.basicConfig(
    stream=sys.stdout, level=logging.DEBUG,
    format=log_format, datefmt="%Y-%m-%d %H:%M:%S"
)


class TodoService(todo_pb2_grpc.TodoServiceServicer):

    def GetUsers(self, request, context):
        users = session.query(User).all()
        userslist_pb = []
        for user in users:
            userslist_pb.append(
                User_pb2(
                    id=user.id,
                    name=user.name,
                    email=user.email
                )
            )
        return UsersList(users=userslist_pb)

    def GetUser(self, request, context):
        user_id = request.id
        user = session.query(User).filter(User.id == user_id).first()
        user_pb2 = User_pb2()

        if user:
            user_pb2.id = user.id
            user_pb2.name = user.name
            user_pb2.email = user.email

        return user_pb2

    def GetUserTodos(self, request, context):
        user_id = request.id
        user = session.query(User).filter(User.id == user_id).first()
        if user:
            todos = user.todos
            todos_pb2 = []
            for todo in todos:
                todos_pb2.append(Todo_pb2(**self._row2dict(todo)))
        else:
            return TodosList()

        return TodosList(todos=todos_pb2)

    def GetTodo(self, request, context):
        pass

    def CreateUser(self, request, context):
        pass

    def CreateTodo(self, request, context):
        pass

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
