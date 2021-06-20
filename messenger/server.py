import select
import socket
from time import time
import pickle
import argparse
import logging.config
from decorators import log

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


@log
def init() -> socket:
    """Init socket for server of messaging."""

    addr, port = get_args()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((addr, port))
    try:
        s.listen()
        s.settimeout(0.2)
    except OSError as error:
        logger.critical(f'Socket was not initiated with next error: {error}')
    else:
        logger.info(f'Server started.')
        return s


@log
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


@log
def set_response(request: dict) -> bytes:
    """Form response for sending to client."""

    actions = {
        'presence': 200,
    }
    result = b''

    try:
        action = request.get('action')
    except AttributeError:
        logger.error('The data to send is not dictionary. ')
    except Exception as error:
        logger.error(f'Unexpected error: {error}')
    else:
        if action == 'msg':
            data = request
        else:
            code = actions[action] if action else 400
            data = prepare_response(code)
        try:
            result = pickle.dumps(data)
        except pickle.PicklingError:
            logger.error('Cannot pack message for sending to a client.')
    return result


@log
def read_requests(r_clients: list, all_clients: list) -> dict:
    """ Read requests from clients."""

    requests = {}

    for sock in r_clients:
        try:
            requests[sock] = pickle.loads(sock.recv(1024))
            print(requests[sock])
        except (pickle.UnpicklingError, TypeError):
            logger.error('Cannot unpack message getting from client.')
        except:
            logger.info(
                f'Client {sock.fileno()} {sock.getpeername()} disconnected.')
            all_clients.remove(sock)

    return requests


@log
def write_responses(requests: dict, w_clients: list,
                    all_clients: list) -> None:
    """Answer clients who sent requests."""

    for sock in w_clients:
        if sock in requests:
            try:
                resp = set_response(requests[sock])
                sock.send(resp)
            except:
                logger.info(f'Client {sock.fileno()} {sock.getpeername()}'
                            f' disconnected.')
                sock.close()
                all_clients.remove(sock)


@log
def process(sock: socket) -> None:
    """Main server process."""

    clients = []

    while True:
        try:
            conn, addr = sock.accept()
        except OSError:
            pass
        else:
            logger.info(f'Connection request from {addr} received.')
            clients.append(conn)
        finally:
            r = []
            w = []
            try:
                r, w, e = select.select(clients, clients, [])
            except:
                pass

            requests = read_requests(r, clients)
            if requests:
                write_responses(requests, w, clients)


def main() -> None:
    server = init()
    process(server)


if __name__ == '__main__':
    main()
