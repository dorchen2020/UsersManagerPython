# ============================ simulation test script ============================
# run this file to run the simulation, in run time don't touch anything
# run server in single command: os.system("start /B start cmd.exe @cmd /k python3 server_tcp.py")
# run client in single command: os.system("start /B start cmd.exe @cmd /k python3 client_tcp.py")


import os
import time
from pynput.keyboard import Key, Controller


def open_cmd_window(file_to_run_from_cmd, width, height):
    try:
        os.system("start /B start cmd.exe")
        time.sleep(1)
        keyboard.type(f"mode con lines={height} cols={width}")
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
        keyboard.type(file_to_run_from_cmd)
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
    except Exception as e:
        print(e)


def execute_command(command):
    try:
        keyboard.type(command)
        time.sleep(1)
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
        time.sleep(2)
    except Exception as e:
        print(e)


def execute_command_multiple_times(command, count_execute):
    try:
        for i in range(1, count_execute):
            keyboard.type(command)
            time.sleep(1)
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)
            time.sleep(2)
    except Exception as e:
        print(e)


keyboard = Controller()

open_cmd_window('python3 server_service/server_tcp.py', 80, 100)  # run server
open_cmd_window('python3 client_service/client_tcp.py', 80, 100)  # run client
time.sleep(2)

# add first user
execute_command('1')
execute_command('Dor')
execute_command('1234')
execute_command('4')

# add user false validation
execute_command('1')
execute_command('Max')
execute_command('123456789')

# add second user
execute_command('Max')
execute_command('abc123')
execute_command('4')

# add exists user (not allowed)
execute_command('1')
execute_command('Dor')
execute_command('1234')
execute_command('4')

# play with Dor user
execute_command('3')
execute_command('Dor')
execute_command_multiple_times('2', 10)
execute_command('-1')

# play with Max user
execute_command('3')
execute_command('Max')
execute_command_multiple_times('2', 6)
execute_command('-1')

# score updated
execute_command('4')

# delete user that does not exist
execute_command('2')
execute_command('Lital')

# delete all users
execute_command('2')
execute_command('Dor')

execute_command('2')
execute_command('Max')

# server without users:
execute_command('4')












