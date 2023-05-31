import json
import sys
import time
import zmq
import socket
from modules.ch341_linux_api import ONET8501


def start_sever():
    try:
        config = sys.argv[1]
    except IndexError:
        bus = 17

    context = zmq.Context()
    socket_zmq = context.socket(zmq.REP)
    port = 5555
    socket_zmq.bind(f"tcp://*:{port}")
    print(f'ip = {socket.gethostbyname(socket.gethostname())}:{port}')

    try:
        onet = ONET8501(bus_=bus, address=0x44)
        status_ = True
    except Exception:
        print(f"just server i2c {bus} not found")
        status_ = False

    while True:
        #  Wait for next request from client
        message = socket_zmq.recv_json()
        print(f"Received request: {message}")

        dict_to_send = {'out': None}
        if status_:
            onet.writeReg(message['address'], message['value'])
            dict_to_send['out'] = onet.readReg(message['address'])

        time.sleep(0.2)
        #  Send reply back to client
        socket_zmq.send_json(json.dumps(dict_to_send))

if __name__ == '__main__':
    start_sever()
