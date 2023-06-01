import json
import sys
import zmq

context = zmq.Context()

#  Socket to talk to server
try:
    ip = sys.argv[1]
except IndexError:
    ip = 'localhost'
    print(f'ip = {ip}')

print("Connecting to hello world server…")
socket = context.socket(zmq.REQ)
socket.connect(f"tcp://{ip}:5555")

#  Do 10 requests, waiting each time for a response
for request in range(100):
    if request % 2:
        dict_to_send = {'reg_address': 0x06,
                        'value': 0x00,
                        'just_get': 1}
    else:
        dict_to_send = {'reg_address': 0x06,
                        'value': 0x00,
                        'just_get': 0}

    print(f"Sending request {request} …")
    socket.send_json(json.dumps(dict_to_send))

    #  Get the reply.
    message = socket.recv_json()
    print(f"Received reply {request} [ {message} ]")
