import socket
import protocol_chat_lib
import users

# AF_INET: using IP protocol (connect IP to IP).
# SOCK_STREAM: using TCP protocol (reliable data transport).

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Server listening to IP and port.
server_socket.bind(('0.0.0.0', 8820))
server_socket.listen()
print("Server is up and running")

# wait for connection in (clients), accept connection and save client data.
# client_socket - object that contains data that server can use to get client
# client_address - tuple that contains IP and port (info also in client_socket object).
(client_socket, client_address) = server_socket.accept()
print('Client connected\n')
username = ""

while True:
    protocol_message = client_socket.recv(1024).decode()  # from bytes to textual string
    print(f"Client sent   : {protocol_message}")
    cmd, data = protocol_chat_lib.extract_protocol_message(protocol_message)
    if cmd == "QUIT":
        print("closing client socket now...")
        protocol_chat_lib.build_and_send_message(client_socket, 'END_OF_PROGRAM', "", False)
    elif cmd == 'ADD_USER':
        if len(data) <= 17:  # just for server validation
            username, password = data.split(sep=protocol_chat_lib.DATA_DELIMITER)
            is_user_exist = users.is_username_exist(username)
            if not is_user_exist:
                users.add_user(username, password)
                protocol_chat_lib.build_and_send_message(client_socket, 'USER_ADDED', "", False)
            else:
                protocol_chat_lib.build_and_send_message(client_socket, 'USER_AL_ADDED', "", False)
        else:  # actually not run because client size validation
            protocol_chat_lib.build_and_send_message(client_socket, 'ADD_USER_FAIL', "", False)
    elif cmd == 'DELETE_USER':
        username = data
        if users.is_username_exist(username):
            users.remove_user(username)
            protocol_chat_lib.build_and_send_message(client_socket, 'USER_DELETED', "", False)
        else:
            protocol_chat_lib.build_and_send_message(client_socket, 'USER_NOT_FOUND', "", False)
    elif cmd == 'CHOOSE_USER':
        username = data
        if users.is_username_exist(username):
            protocol_chat_lib.build_and_send_message(client_socket, 'USERNAME_EXIST', "", False)
        else:
            protocol_chat_lib.build_and_send_message(client_socket, 'USER_NOT_FOUND', "", False)
    elif cmd == 'UPDATE_SCORE':
        score = int(data.split(sep=protocol_chat_lib.DATA_DELIMITER)[1])
        # update user score in list
        for user in users.users_list:
            if user.username == username:
                user.add_score(score)
        protocol_chat_lib.build_and_send_message(client_socket, 'SCORE_UPDATED', "", False)

    elif cmd == 'GET_ALL_USERS':
        my_list = users.users_list_to_string()
        if not my_list:
            protocol_chat_lib.build_and_send_message(client_socket, 'EMPTY_LIST', "", False)
            continue
        print('Server answer :')
        print(my_list)
        my_list = my_list.encode()
        client_socket.send(my_list)
    else:
        print('invalid command')
# client_socket.close()
# server_socket.close()

