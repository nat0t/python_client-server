import socket
from time import time
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
def set_request() -> Union[str, bytes, None]:
    """Form request for sending to server."""

    action, src, dst = 'msg', 'Vasya', '*'

    msg = input('Your message: ')
    if msg == 'exit':
        logger.info(f'Connection closed.')
        return 'exit'
    request = {
        'action': action,
        'time': time(),
        'to': dst,
        'from': src,
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
def read_responses(conn: socket) -> None:
    while True:
        data = get_response(conn.recv(1024))
        print(data['message'])


@log
def write_requests(conn: socket) -> None:
    while True:
        data = set_request()
        if data:
            if data == 'exit':
                break
            conn.send(data)
        else:
            logger.info('No data to sending.')


@log
def main():
    conn = init()
    if conn:
        mode = input('Select mode (r/w): ')
        try:
            if mode == 'r':
                read_responses(conn)
            elif mode == 'w':
                write_requests(conn)
        except Exception as error:
            logger.error(f'Unexpected error: {error}')


if __name__ == '__main__':
    main()
