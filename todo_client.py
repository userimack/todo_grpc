import grpc
import sys

import todo_pb2
import todo_pb2_grpc

import logging

log_format = '%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s'
logging.basicConfig(
    stream=sys.stdout, level=logging.DEBUG,
    format=log_format, datefmt="%Y-%m-%d %H:%M:%S"
)


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


def send_email(subject, body):
    logging.info("Stub for sending mail.")


def get_todo(todo_id):
    try:
        stub.GetTodo(todo_pb2.Todo(id=todo_id))
    except grpc.RpcError as e:
        error_message = e.details()
        status_code = e.code()
        logging.error(error_message)
        send_email(subject="Todo - {} - StatusCode: {}".format("get_todo",
                   status_code.name), body=error_message)

    except Exception as e:
        print(e.details())
        status_code = e.code()
        print(status_code.name)
        print(status_code.value)
