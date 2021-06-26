import socket
import sys
from threading import Thread
from time import time, sleep
import pickle
import argparse
import logging.config

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
def write_request(conn: socket, action: str, **kwargs) -> None:
    """Send request to server with specified action."""

    request = {}
    if action == 'presence':
        request = {
            'action': 'presence',
            'time': time(),
            'account_name': kwargs['account_name'],
        }
    elif action == 'join':
        request = {
            'action': 'join',
            'time': time(),
            'room': kwargs['room'],
        }
    elif action == 'leave':
        request = {
            'action': 'leave',
            'time': time(),
            'room': kwargs['room'],
        }
    elif action == 'msg':
        request = {
            'action': 'msg',
            'time': time(),
            'to': kwargs['to'],
            'from': kwargs['from_'],
            'message': kwargs['msg']
        }

    if request:
        try:
            conn.send(pickle.dumps(request))
        except pickle.PicklingError:
            logger.error('Cannot pack message for sending to server.')
        except OSError:
            logger.error('Cannot send message to server.')


@log
def get_response(data: bytes) -> dict:
    """Unpack response getting from server."""

    response = {}
    try:
        response = pickle.loads(data)
    except pickle.UnpicklingError:
        logger.error('Cannot unpack message getting from server.')
    except Exception as error:
        logger.error(f'Unexpected error: {error}')
    return response


@log
def read_responses(conn: socket) -> None:
    """Receive messages from server and print it."""

    while True:
        try:
            response = get_response(conn.recv(1024))
        except OSError:
            logger.warning('Server is not available. Client is stopping...')
            sys.exit(0)

        if response.get('action') == 'msg':
            print(f'Sender {response["from"]}\nMessage: {response["message"]}')


@log
def main() -> None:
    """Main process of messenger's client."""

    try:
        conn = init()
        print('Welcome to our messenger. If you want to stop, type "exit".')
        account_name = input('Type your nickname: ')
        write_request(conn, 'presence', account_name=account_name)
        room = input('Type name of your chat: ')
        write_request(conn, 'join', room=room)

        read = Thread(target=read_responses, args=(conn,))
        read.daemon = True
        read.start()

        while True:
            sleep(0.5)
            msg = input('Your message: ')
            if msg == 'exit':
                break
            write_request(conn, 'msg', to=room, from_=account_name, msg=msg)
    except Exception as error:
        logger.error(f'Unexpected error: {error}')


if __name__ == '__main__':
    main()
