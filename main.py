# file in process

from server_service import server_tcp
from client_service import client_tcp
import os


def run_server():
    os.system('server_tcp')


def run_client():
    os.system('client_tcp')


if __name__ == '__main__':
    run_server()
    run_client()
