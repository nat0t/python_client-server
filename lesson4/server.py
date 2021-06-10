import socket
from time import time
import pickle
import argparse


def get_args():
    """Get arguments for server starting. """

    parser = argparse.ArgumentParser(
        description='Messenger startup settings')
    parser.add_argument('-a', action='store', dest='addr', default='0.0.0.0',
                        help='Listening address')
    parser.add_argument('-p', action='store', dest='port', type=int, default=7777,
                        help='Listening port')
    args = parser.parse_args()
    return args.addr, args.port


def init() -> socket:
    """Init socket for server of messaging."""

    addr, port = get_args()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((addr, port))
    try:
        s.listen()
    except OSError as error:
        print(f'Socket was not initiated with next error:\n{error}')
    else:
        print(f'Server is running on {addr}:{port}...')
        return s


def get_request(data: bytes) -> dict:
    """Unpack request getting from client."""

    try:
        request = pickle.loads(data)
    except pickle.UnpicklingError:
        print('Cannot unpack message getting from client.')
        request = {}
    return request


def prepare_response(code: int) -> dict:
    """Prepare answer based on getting code."""

    alerts = {
        200: 'OK',
        202: 'Accepted',
        400: 'Bad request',
    }

    return {
        'response': code,
        'time': time(),
        'alert': alerts[code]
    }


def set_response(request: dict) -> bytes:
    """Form response for sending to client."""

    actions = {
        'presence': 200,
        'stop': 202,
    }

    action = request.get('action')
    code = actions[action] if action else 400
    try:
        return pickle.dumps(prepare_response(code))
    except pickle.PicklingError:
        print('Cannot pack message for sending to client.')
        return b''


def process(sock: socket) -> None:
    """Main server process."""

    msg_max_size = 640

    while True:
        conn, _ = sock.accept()
        try:
            data = conn.recv(msg_max_size)
        except socket.timeout:
            print('Socket was timed out. Server stopped.')
        except OSError as error:
            print(f'Unexpected error:\n{error}')
        else:
            request = get_request(data)
            print(request)

            response = set_response(request)
            if response:
                conn.send(response)
                conn.close()

            if request['action'] == 'stop':
                print('Server stopping...')
                break


def main() -> None:
    server = init()
    process(server)


if __name__ == '__main__':
    main()
