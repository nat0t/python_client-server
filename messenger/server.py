import select
import socket
from time import time
import pickle
import argparse
import logging.config
from typing import Tuple

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
def prepare_response(code: int, user: str) -> dict:
    """Prepare answer based on getting code."""

    alerts = {
        200: 'OK',
        202: 'Accepted',
        400: 'Bad request',
        401: 'Unauthorized',
        402: 'Wrong user/password',
        404: 'Not found'
    }
    alert = alerts.get(code)
    result = {'response': code, 'time': time(), 'alert': alert, 'user': user}
    return result if alert else None


@log
def set_response(request: dict, db: dict) -> Tuple[dict, dict]:
    """Form response for sending to client."""

    actions = {
        'presence': 200,
        'msg': 200,
        'authenticate': 200,
        'join': 202,
        'leave': 202,
    }
    result = b''

    try:
        action = request.get('action')
        user = request.get('user')
    except AttributeError:
        logger.error('The data to send is not dictionary. ')
    except Exception as error:
        logger.error(f'Unexpected error: {error}')
    else:
        if action == 'authenticate':
            if user in db['users'] and request['password'] == db['users'][user]:
                code = actions[action]
            else:
                code = 402
        elif action in ('join', 'leave'):
            room = request.get('room')
            if room in db['rooms']:
                if action == 'join':
                    db['rooms'][room].append(user)
                else:
                    db['rooms'][room].remove(user)
                code = actions[action]
            else:
                code = 404
        elif action == 'msg':
            return request, db
    result = prepare_response(code, user)
    return result, db


@log
def read_requests(r_clients: list, all_clients: list) -> Tuple[dict, dict]:
    """ Read requests from clients."""

    requests = {}
    users = {}

    for sock in r_clients:
        try:
            requests[sock] = pickle.loads(sock.recv(1024))
            user = requests[sock]['user']
            users[user] = sock
        except (pickle.UnpicklingError, TypeError):
            logger.error('Cannot unpack message getting from client.')
        except:
            logger.info(
                f'Client {sock.fileno()} {sock.getpeername()} disconnected.')
            all_clients.remove(sock)

    return requests, users


@log
def write_responses(requests: dict, w_clients: list,
                    all_clients: list, db: dict, users: dict) -> dict:
    """Answer clients who sent requests."""

    for sock in w_clients:
        if sock in requests:
            try:
                resp = pickle.dumps(set_response(requests[sock], db))
            except pickle.PicklingError:
                logger.error('Cannot pack message for sending to a client.')
            else:
                try:
                    action = requests[sock].get('action')
                    if action == 'msg':
                        to = requests[sock].get('to')
                        if to.startswith('#'):
                            for user in db['rooms'][to][1:]:
                                users[user].send(resp)
                        else:
                            user = db['users'][to]
                            users[user].send(resp)
                    else:
                        print(sock)
                        sock.send(resp)
                except:
                    logger.info(f'Client {sock.fileno()} {sock.getpeername()}'
                                f' disconnected.')
                    sock.close()
                    all_clients.remove(sock)
        return db


@log
def process(sock: socket) -> None:
    """Main server process."""

    db = {
        'users': {'u1': 'p1', 'u2': 'p2', 'u3': 'p3'},
          'rooms': {'r1': [], 'r2': []}
    }
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

            requests, users = read_requests(r, clients)
            if requests:
                db = write_responses(requests, w, clients, db, users)


def main() -> None:
    server = init()
    process(server)


if __name__ == '__main__':
    main()
