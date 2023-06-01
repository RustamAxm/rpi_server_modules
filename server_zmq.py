import json
import sys
import time
import zmq
import socket
import yaml
import Adafruit_ADS1x15
from modules.ch341_linux_api import SmBusWrapper


def write_to_onet(onet, message):
    try:
        onet.writeReg(message['reg_address'], message['value'])
        return onet.readReg(message['reg_address'])
    except Exception as err:
        print(f'{err} in write to bus')
        return err.args


def read_in_onet(onet):
    data = []
    for i in range(16):
        tmp = None
        try:
            tmp = onet.readReg(i)
        except Exception as err:
            print(f'{err} in write to bus')
            tmp = err.args
        data.append(tmp)

    return data


def get_adc_data(adc, gain=1):
    data = []
    for i in range(4):
        data.append(adc.read_adc(i, gain=gain))

    return data


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
        print(f"config = {config}")

    adc = None
    try:
        adc = Adafruit_ADS1x15.ADS1015(address=config['address_adc'], busnum=config['bus'])
    except Exception:
        print(f"just server i2c-ADC {config['bus']} or 0x48 not found")

    onet = None
    try:
        onet = SmBusWrapper(bus_=config['bus'], address=config['address_onet'])
    except Exception:
        print(f"just server i2c {config['bus']} or {config['address_onet']} not found")

    while True:
        #  Wait for next request from client
        message = json.loads(socket_zmq.recv_json())
        print(f"Received request: {message}")

        dict_to_send = {'onet_out': None,
                        'adc_out': None}
        time.sleep(0.1)
        if message['just_get']:
            dict_to_send['adc_out'] = get_adc_data(adc)
            dict_to_send['onet_out'] = read_in_onet(onet)
            socket_zmq.send_json(json.dumps(dict_to_send))
            continue
        else:
            if onet is not None:
                dict_to_send['onet_out'] = write_to_onet(onet, message)

            if adc is not None:
                dict_to_send['adc_out'] = get_adc_data(adc)

            #  Send reply back to client
            socket_zmq.send_json(json.dumps(dict_to_send))


if __name__ == '__main__':
    start_sever()
