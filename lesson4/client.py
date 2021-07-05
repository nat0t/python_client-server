import socket
from time import time
import pickle
import argparse


def get_args():
    """Get arguments for server starting. """

    parser = argparse.ArgumentParser(
        description='Messenger startup settings')
    parser.add_argument('addr', help='Server address')
    parser.add_argument('port', type=int, help='Server port')
    args = parser.parse_args()
    return args.addr, args.port


def init() -> socket:
    """Init socket for messenger client."""

    addr, port = get_args()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((addr, port))
    except ConnectionRefusedError:
        print('Failed to establish connection with server.')
    except OSError as error:
        print(f'Socket was not initiated with next error:\n{error}')
    else:
        return s


def set_request(action: str, user: str, status: str = None) -> bytes:
    """Form request for sending to server."""

    requests = {
        'presence': {
            'action': action,
            'time': time(),
            'type': 'status',
            'user': {
                'account_name': user,
                'status': status
            }
        },
        'stop': {
            'action': action
        }
    }

    request = requests.get(action)
    try:
        return pickle.dumps(request) if request else None
    except pickle.PicklingError:
        print('Cannot pack message for sending to server.')
        return b''


def get_response(data: bytes) -> dict:
    """Unpack response getting from server."""

    response = {}
    try:
        response = pickle.loads(data)
    except pickle.UnpicklingError:
        print('Cannot unpack message getting from server.')
    except TypeError:
        print('Got not bytes-like object for unpacking.')
    except Exception as error:
        print(f'Unexpected error:\n{error}')
    return response


def main():
    msg_max_size = 100
    actions = ('presence', 'stop')
    user = 'Vasya'
    status = 'I am still here'

    for action in actions:
        request = set_request(action, user, status)
        conn = init()
        if conn and request:
            conn.send(request)
            try:
                data = conn.recv(msg_max_size)
            except ConnectionError:
                print('Connection error.')
            except Exception as error:
                print(f'Unexpected error:\n{error}')
            else:
                response = get_response(data)
                print(response)


if __name__ == '__main__':
    main()
