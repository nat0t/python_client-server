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
def get_request(data: bytes) -> dict:
    """Unpack request getting from client."""

    request = {}
    try:
        request = pickle.loads(data)
    except pickle.UnpicklingError:
        logger.error('Cannot unpack message getting from server.')
    except Exception as error:
        logger.error(f'Unexpected error: {error}')
    return request


@log
def set_response(request: dict) -> bytes:
    """Form response for sending to client."""

    action = request.get('action')
    response = {
        'response': 400,
        'time': time(),
        'alert': 'Bad request'
    }
    if action == 'presence':
        response = {
            'response': 200,
            'time': time(),
            'alert': 'Successfully joined to server.'
        }
    elif action == 'join':
        response = {
            'response': 200,
            'time': time(),
            'alert': f'Successfully joined to room {request.get("room")}.'
        }
    elif action == 'msg':
        response = {
            'response': 200,
            'action': 'msg',
            'time': time(),
            'from': request.get('from'),
            'to': 'all',
            'message': request.get('message')
        }

    print(response)
    try:
        data = pickle.dumps(response)
    except pickle.PicklingError:
        logger.error('Cannot pack message for sending to server.')
    else:
        logger.info(f'Responded with code {response["response"]}.')
        return data


@log
def read_requests(r_clients: list, all_clients: list) -> list:
    """ Read requests from clients."""

    responses = []

    for client in r_clients:
        try:
            request = get_request(client.recv(1024))
            print(request)
            responses.append(set_response(request))
        except OSError:
            all_clients.remove(client)
            logger.info(f'Connection with {client} was dropped.')
    return responses


@log
def write_responses(responses: list, w_clients: list,
                    all_clients: list) -> None:
    """Answer clients who sent requests."""

    for response in responses:
        for client in w_clients:
            try:
                client.send(response)
            except ConnectionError:
                client.close()
                all_clients.remove(client)
                logger.info(f'Connection with {client} was dropped.')


@log
def process(sock: socket) -> None:
    """Main messenger's server process."""

    clients = []

    while True:
        try:
            conn, addr = sock.accept()
        except OSError:
            pass
        else:
            logger.info(f'Received connection from {addr}.')
            clients.append(conn)
        finally:
            r = []
            w = []
            try:
                r, w, e = select.select(clients, clients, [])
            except:
                pass

            responses = read_requests(r, clients)
            if responses:
                write_responses(responses, w, clients)


def main() -> None:
    server = init()
    process(server)


if __name__ == '__main__':
    main()
