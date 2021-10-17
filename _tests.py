# pytest _tests.py -v               =>     run all tests
# pytest _tests.py -m smoke -v      =>     run smoke tests
import pytest

from protocol_chat_lib import build_protocol_message, extract_protocol_message


@pytest.mark.smoke
def test_smoke_build_protocol_1():
    assert build_protocol_message("SOME_COMMAND", ['data1']) == 'SOME_COMMAND    |0005|data1', \
        'Fail in smoke test 1'


@pytest.mark.smoke
def test_smoke_build_protocol_2():
    assert build_protocol_message("SOME_COMMAND", ['data1', 'data2']) == 'SOME_COMMAND    |0011|data1#data2', \
        'Fail in smoke test 2'


@pytest.mark.smoke
def test_smoke_extract_protocol_1():
    assert extract_protocol_message('CHOOSE_USER     |0003|dor') == ('CHOOSE_USER', 'dor'), \
        'Fail in smoke test 3'


@pytest.mark.smoke
def test_smoke_extract_protocol_2():
    assert extract_protocol_message('CHOOSE_USER     |0008|dor#1234') == ('CHOOSE_USER', 'dor#1234'), \
        'Fail in smoke test 4'


def test_build_protocol_1():
    assert build_protocol_message("ADD_USER", ['dor', '1234']) == 'ADD_USER        |0008|dor#1234', \
        'Fail in build ADD_USER protocol'


def test_build_protocol_2():
    assert build_protocol_message("CHOOSE_USER", ['dor']) == 'CHOOSE_USER     |0003|dor', \
        'Fail in build CHOOSE_USER protocol'


def test_build_protocol_3():
    assert build_protocol_message("UPDATE_SCORE", []) == 'UPDATE_SCORE    |0000|', \
        'Fail in build UPDATE_SCORE protocol'


def test_build_protocol_4():
    assert build_protocol_message("GET_ALL_USERS", []) == 'GET_ALL_USERS   |0000|', \
        'Fail in build GET_ALL_USERS protocol'


def test_build_protocol_5():
    assert build_protocol_message("QUIT", []) == 'QUIT            |0000|', \
        'Fail in build QUIT protocol'


def test_extract_protocol_6():
    assert extract_protocol_message('ADD_USER        |0008|dor#1234') == ('ADD_USER', 'dor#1234'), \
        'Fail in extract ADD_USER protocol'


def test_extract_protocol_7():
    assert extract_protocol_message('DELETE_USER     |0003|dor') == ('DELETE_USER', 'dor'), \
        'Fail in extract DELETE_USER protocol'


def test_extract_protocol_8():
    assert extract_protocol_message('CHOOSE_USER     |0003|dor') == ('CHOOSE_USER', 'dor'), \
        'Fail in extract CHOOSE_USER protocol'

