import socket
from threading import Thread
from queue import Queue
from time import time, sleep
import pickle
import argparse
import logging.config
from typing import Union

from decorators import log

logging.config.fileConfig('logging.ini')
logger = logging.getLogger('messenger.client')


def get_args():
    """Get arguments for server starting. """

    parser = argparse.ArgumentParser(
        description='Messenger startup settings')
    parser.add_argument('addr', help='Server address')
    parser.add_argument('port', type=int, help='Server port')
    args = parser.parse_args()
    return args.addr, args.port


@log
def init() -> socket:
    """Init socket for messenger client."""

    addr, port = get_args()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    logger.info(f'Trying to connect to {addr}:{port}.')
    try:
        s.connect((addr, port))
    except ConnectionRefusedError:
        logger.critical('Failed to establish connection with server.')
    except OSError as error:
        logger.critical(f'Socket was not initiated with next error: {error}')
    else:
        logger.info(f'Connected to {addr}:{port}.')
        return s


@log
def set_request(flow: Queue) -> Union[str, bytes, None]:
    """Form request for sending to server."""

    # Get data from server
    try:
        response = flow.get_nowait()
    except:
        response = {}
    request = ''
    user = response.get('user') if 'user' in response else 'guest'

    sleep(0.5)
    menu = {
        'guest': '1. Send message to user as guest.\n'
                 '2. Authenticate.\n',
        'non-guest': '1. Send message to user.\n'
                     '2. Join to room.\n'
                     '3. Quit from room.\n'
                     '4. Send message to room.\n'}
    action = input(
        f'Choose your action, {user}:\n{menu["guest"] if user == "guest" else menu["non-guest"]}0. Quit from server.\n')
    if action == '0':
        # Disconnect from server
        logger.info(f'Connection closed.')
        return 'exit'
    elif action == '1':
        # Send message
        to = input('Who do you want to send the message to? ')
        msg = input('Your message: ')
        request = {
            'action': 'msg',
            'time': time(),
            'to': to,
            'user': user,
            'message': msg
        }
    elif action == '2':
        # Authenticate
        if user == 'guest':
            user = input('Input your nickname: ')
            password = input('Input your password: ')
            request = {
                'action': 'authenticate',
                'time': time(),
                'user': user,
                'password': password
            }
        else:
            # Join to room
            room = input('Input name of room: ')
            request = {
                'action': 'join',
                'time': time(),
                'room': room,
                'user': user
            }
    elif action == '3':
        # Quit from room
        room = input('Input name of room: ')
        request = {
            'action': 'leave',
            'time': time(),
            'room': room,
            'user': user
        }
    elif action == '4':
        # Send message to room
        room = input('Input name of room: ')
        msg = input('Your message: ')
        request = {
            'action': 'msg',
            'time': time(),
            'to': f"#{room}",
            'from': user,
            'message': msg
        }

    try:
        return pickle.dumps(request) if request else None
    except pickle.PicklingError:
        logger.error('Cannot pack message for sending to server.')
        return b''


@log
def get_response(data: bytes) -> dict:
    """Unpack response getting from server."""

    response = {}
    try:
        response = pickle.loads(data)
    except pickle.UnpicklingError:
        logger.error('Cannot unpack message getting from server.')
    except TypeError:
        logger.error('Got not bytes-like object for unpacking.')
    except Exception as error:
        logger.error(f'Unexpected error: {error}')
    else:
        logger.info(f'Server successfully responded.')
    return response


@log
def read_responses(conn: socket, flow: Queue) -> None:
    while True:
        data = get_response(conn.recv(1024))
        print(data['message'])
        print(data)
        flow.put(data)


@log
def write_requests(conn: socket, flow: Queue) -> None:
    while True:
        data = set_request(flow)
        if data:
            if data == 'exit':
                break
            conn.send(data)
        else:
            logger.info('No data to sending.')


@log
def main():
    conn = init()
    try:
        if conn:
            flow = Queue()
            read = Thread(target=read_responses, args=(conn, flow))
            read.daemon = True
            read.start()
            write_requests(conn, flow)
    except Exception as error:
        logger.error(f'Unexpected error: {error}')


if __name__ == '__main__':
    main()
