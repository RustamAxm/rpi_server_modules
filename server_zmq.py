import json
import sys
import time
import zmq
import socket
import yaml
from modules.ch341_linux_api import ONET8501


def write_to_i2c(onet, message):
    try:
        onet.writeReg(message['reg_address'], message['value'])
        return onet.readReg(message['reg_address'])
    except Exception as err:
        print(f'{err} in write to bus')
        return err.args


def start_sever():
    try:
        config_path = sys.argv[1]
    except IndexError:
        config_path = 'config.yaml'

    context = zmq.Context()
    socket_zmq = context.socket(zmq.REP)
    port = 5555
    socket_zmq.bind(f"tcp://*:{port}")
    print(f'ip = {socket.gethostbyname(socket.gethostname())}:{port}')

    with open(config_path, 'r') as conf:
        config = yaml.full_load(conf)
        print(f"i2c bus = {config['bus']}, address = {config['address']}")

    try:
        onet = ONET8501(bus_=config['bus'], address=config['address'])
        status_ = True
    except Exception:
        print(f"just server i2c {config['bus']} or {config['address']} not found")
        status_ = False

    while True:
        #  Wait for next request from client
        message = json.loads(socket_zmq.recv_json())
        print(f"Received request: {message}")

        dict_to_send = {'out': None}
        if status_:
            dict_to_send['out'] = write_to_i2c(onet, message)

        time.sleep(0.2)
        #  Send reply back to client
        socket_zmq.send_json(json.dumps(dict_to_send))

if __name__ == '__main__':
    start_sever()
