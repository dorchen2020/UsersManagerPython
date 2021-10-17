import client

conn = client.connect()

try:
    while True:
        msg = input("Command Options:\n1. Add User \n2. Delete User \n3. Choose User And Play  \n"
                    "4. Print All Users  \n5. Quit\nEnter command number:\n ")
        if msg == '1':
            client.add_user(conn)
        elif msg == '2':
            client.delete_user(conn)
        elif msg == '3':
            client.choose_user_and_play(conn)
        elif msg == '4':
            client.print_all_users(conn)
        elif msg == '5':
            client.quit_server(conn)
        else:
            print("invalid selection... select a number\n")
except ConnectionResetError as cre:
    print(f"ConnectionResetError: {cre}")
except Exception as e:
    print(e)
