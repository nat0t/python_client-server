import socket
from time import time
import pickle
import argparse
import logging.config
from decorators import get_caller_name

logging.config.fileConfig('logging.ini')
logger = logging.getLogger('messenger.server')


def get_args():
    """Get arguments for server starting. """

    parser = argparse.ArgumentParser(
        description='Messenger startup settings')
    parser.add_argument('-a', action='store', dest='addr', default='0.0.0.0',
                        help='Listening address')
    parser.add_argument('-p', action='store', dest='port', type=int,
                        default=7777, help='Listening port')
    args = parser.parse_args()
    return args.addr, args.port


@get_caller_name()
def init() -> socket:
    """Init socket for server of messaging."""

    addr, port = get_args()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((addr, port))
    try:
        s.listen()
    except OSError as error:
        logger.critical(f'Socket was not initiated with next error: {error}')
    else:
        logger.info(f'Server started.')
        return s


@get_caller_name()
def get_request(data: bytes) -> dict:
    """Unpack request getting from client."""

    request = {}
    try:
        request = pickle.loads(data)
    except pickle.UnpicklingError:
        logger.error('Cannot unpack message getting from client.')
    except TypeError:
        logger.error('Got not bytes-like object for unpacking.')
    except Exception as error:
        logger.error(f'Unexpected error: {error}')
    else:
        logger.info(f'Client sent {request["action"]}-message.')
    return request


@get_caller_name()
def prepare_response(code: int) -> dict:
    """Prepare answer based on getting code."""

    alerts = {
        200: 'OK',
        202: 'Accepted',
        400: 'Bad request',
    }
    alert = alerts.get(code)
    result = {'response': code, 'time': time(), 'alert': alert}
    return result if alert else None


@get_caller_name()
def set_response(request: dict) -> bytes:
    """Form response for sending to client."""

    actions = {
        'presence': 200,
        'stop': 202,
    }
    result = b''

    try:
        action = request.get('action')
    except AttributeError:
        logger.error('The data to send is not dictionary. ')
    except Exception as error:
        logger.error(f'Unexpected error: {error}')
    else:
        code = actions[action] if action else 400
        try:
            result = pickle.dumps(prepare_response(code))
        except pickle.PicklingError:
            logger.error('Cannot pack message for sending to client.')
    return result


@get_caller_name()
def process(sock: socket) -> None:
    """Main server process."""

    msg_max_size = 640

    while True:
        conn, _ = sock.accept()
        try:
            data = conn.recv(msg_max_size)
        except socket.timeout:
            logger.warning('Socket was timed out. Server stopped.')
        except OSError as error:
            logger.error(f'Unexpected error: {error}')
        else:
            request = get_request(data)
            print(request)

            response = set_response(request)
            if response:
                conn.send(response)
                conn.close()
                logger.info(f'Connection closed.')

            if request['action'] == 'stop':
                logger.info('Server stopped.')
                break


def main() -> None:
    server = init()
    process(server)


if __name__ == '__main__':
    main()
