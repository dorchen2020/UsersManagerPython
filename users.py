
import random
import protocol_chat_lib

users_list = []


class Users:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.score = 0

    def print_details(self):
        return f"username: {self.username} | password: {self.password} | score: {self.score}"

    def add_score(self, score):
        self.score += score


def add_user(username, password):
    user = Users(username, password)
    users_list.append(user)


def is_username_exist(username):
    for user in users_list:
        if user.username == username:
            return True
    return False


def remove_user(username):
    for user in users_list:
        if user.username == username:
            users_list.remove(user)
            return True
    return False


def play_with_user(conn, username):
    score = 0
    while True:
        rand_number = random.randint(1, 3)
        try:
            guess_number = int(input('Guess number between 1-3, to quit enter -1\n'))
        except ValueError:
            print('Type mismatch, Guess number between 1-3')
            continue
        if guess_number == -1:
            data = [username, score]
            protocol_chat_lib.build_and_send_message(conn, 'UPDATE_SCORE', data, True)
            cmd, data = protocol_chat_lib.recv_message_and_parse(conn, False)
            if cmd == 'SCORE_UPDATED':
                break

        elif not 1 <= guess_number <= 3:
            print('invalid number, guess number between 1-3\n')
        elif rand_number == guess_number:
            score += 5
            print(f'Good guess, {username} earn 5 scores! currently score is: {score}\n')
            # for user in users_list:
            #     if user.username == username:
            #         user.add_score += 5
                    # print(f'Good guess, {username} earn 5 scores! currently score is: {score}\n')
        else:  # wrong number
            print(f'Wrong guess, try again...\n')
    print(f"Game ends\n")


def print_users():
    if not users_list:
        print('Users list is empty\n')
        return
    print('All Users:')
    for user in users_list:
        print(f'{user.print_details()}')
    print('\n')


def users_list_to_string():
    if not users_list:
        return False
    string_user_list = ''
    for user in users_list:
        string_user_list += \
            f"username: {user.username.ljust(8,' ')} | password: {user.password.ljust(8,' ')} | score: {user.score}\n"
    return string_user_list
