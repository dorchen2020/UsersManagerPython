import socket
import protocol_chat_lib
import users

SERVER_IP = "127.0.0.1"
SERVER_PORT = 8820


def connect():
    # create TCP object
    # AF_INET: using IP protocol (connect IP to IP).
    # SOCK_STREAM: using TCP protocol (reliable data transport).
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # connect to server IP and port (Local host).
    sock.connect((SERVER_IP, SERVER_PORT))
    return sock


def error_and_exit(error_msg):
    print(error_msg)
    exit()


# Get from client user & password, send it in protocol and get answer
def add_user(conn):
    while True:
        username = input("Please insert username (8 characters maximum): \n")
        if len(username) > 8:
            print("max len of username is 8, insert again")
            continue
        password = input("Please insert password (8 characters maximum): \n")
        if len(password) > 8:
            print("max len of password is 8, insert details again")
            continue
        if username.find('#') != -1 or password.find('#') != -1:
            print("'#' is invalid character, insert again...")
            continue
        data = [username, password]
        protocol_chat_lib.build_and_send_message(conn, "ADD_USER", data, True)
        cmd, data = protocol_chat_lib.recv_message_and_parse(conn, False)
        if cmd == 'USER_ADDED' or cmd == 'USER_AL_ADDED':
            return
        else:
            print("try again...")


def delete_user(conn):
    username_to_delete = input("Enter username to delete: \n")
    data = [username_to_delete]
    protocol_chat_lib.build_and_send_message(conn, 'DELETE_USER', data, True)
    cmd, data = protocol_chat_lib.recv_message_and_parse(conn, False)
    if cmd == 'USER_DELETED' or cmd == 'USER_NOT_FOUND':
        return
    else:
        print("try again...")


def choose_user_and_play(conn):
    username_to_play = input("Choose user to play with (enter username):\n")
    data = [username_to_play]
    protocol_chat_lib.build_and_send_message(conn, 'CHOOSE_USER', data, True)
    cmd, data = protocol_chat_lib.recv_message_and_parse(conn, False)

    if cmd == 'USER_NOT_FOUND':
        return
    else:
        print("Game Starts...\n")
        users.play_with_user(conn, username_to_play)


def print_all_users(conn):
    protocol_chat_lib.build_and_send_message(conn, 'GET_ALL_USERS', "", True)
    protocol_message = conn.recv(1024).decode()
    if 'EMPTY_LIST' in protocol_message:
        print(f'Server answer : {protocol_message}\n')
    else:
        print(f'Server answer :\n{protocol_message}')


def quit_server(conn):
    protocol_chat_lib.build_and_send_message(conn, 'QUIT', "", True)
    cmd, data = protocol_chat_lib.recv_message_and_parse(conn, False)
    if cmd == 'END_OF_PROGRAM':
        print("Quit from application, client socket closed")
    else:
        print("response error, forcefully exit...")
    conn.close()
    exit()


