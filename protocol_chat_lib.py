# Protocol Messages

CMD_FIELD_LENGTH = 16  # Exact length of cmd field (in bytes)
DELIMITER = "|"  # Delimiter character in protocol
DATA_DELIMITER = "#"  # Delimiter in the data part of the message


# build protocol message and send it from client to server and opposite
def build_and_send_message(conn, cmd, data, is_client):
	"""
	Builds a new message according to the custom protocol and sends it to the given socket.
	Parameters: conn (socket object), cmd (command str), data (strings list), is_client (who send ths message)
	Returns: nothing
	"""
	# try:
	protocol_msg = build_protocol_message(cmd, data)
	conn.send(protocol_msg.encode())
	if is_client:
		print(f"Client sent   : {protocol_msg}")
	else:
		print(f"Server answer : {protocol_msg}\n")
	# except ConnectionRefusedError as ce:
	# 	print(ce)
	# except Exception as e:
	# 	print(e)


# extract protocol message and send it from client to server and opposite
def recv_message_and_parse(conn, is_client):
	"""
	Receives a new message from given socket, then parses the message.
	Parameters: conn (socket object), is_client (who send ths message)
	Returns: cmd (command str) and data (strings list).
	"""
	# try:
	protocol_msg = conn.recv(1024).decode()
	cmd, data = extract_protocol_message(protocol_msg)
	if is_client:
		print(f"Client sent   : {protocol_msg}")
	else:
		print(f"Server answer : {protocol_msg}\n")
	return cmd, data
	# except ConnectionResetError as cre:
		# print(cre)


def join_data(msg_data):
	"""
	Gets a list, joins all of it's fields to one string divided by the data delimiter.
	Returns: data strings separated by delimiter.
	example: (data1, data2)  =>  'data1#data2'
	"""
	return DATA_DELIMITER.join(map(str, msg_data))
	# same like: return DATA_DELIMITER.join(str(elem) for elem in msg_fields)


def build_protocol_message(cmd, data):
	"""
	Gets command name (str) and data field (list of strings) and creates a valid protocol message
	Returns: protocol message (str), or None if error occurred.
	examples:
	'LOGIN', ('dor','1234') => 'LOGIN           |0008|dor#1234'
	'DELETE_USER', ('dor')  => 'LOGIN           |0008|dor'
	"""

	# try:
	cmd_len = len(cmd)
	data_len_list = len(data)
	if data_len_list == 1:
		data_string = ''.join(data)
	else:
		data_string = join_data(data)  # join items list to str separated by delimiter
	data_len_string = len(data_string)
	if cmd_len > CMD_FIELD_LENGTH or not (0 <= data_len_string <= 9999):
		return None
	next_field_size = str(data_len_string).zfill(4)
	protocol_msg = f"{cmd.ljust(CMD_FIELD_LENGTH, ' ')}{DELIMITER}{next_field_size}{DELIMITER}{data_string}"
	return protocol_msg
	# except Exception as e:
	# 	print(e)


def extract_protocol_message(protocol_message):
	"""
	Extract command and data from protocol message.
	Returns: cmd (command str), data (strings list). If some error occurred, returns None
	example: 'LOGIN     |8|abcd#1234'  =>  cmd = 'LOGIN' , data = 'abcd#1234'
	"""
	# try:
	if protocol_message.count(DELIMITER) != 2:
		return None
	split_list = protocol_message.split(sep=DELIMITER)
	cmd = split_list[0].replace(' ', '')
	data = split_list[2]
	return cmd, data
