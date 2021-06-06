"""
Реализовать простое клиент-серверное взаимодействие по протоколу JIM
(JSON instant messaging):
a. клиент отправляет запрос серверу;
b. сервер отвечает соответствующим кодом результата.
Клиент и сервер должны быть реализованы в виде отдельных скриптов,
содержащих соответствующие функции.
Функции клиента:
* сформировать presence-сообщение;
* отправить сообщение серверу;
* получить ответ сервера;
* разобрать сообщение сервера;
* параметры командной строки скрипта client.py <addr> [<port>]:
  addr — ip-адрес сервера;
  port — tcp-порт на сервере, по умолчанию 7777.
Функции сервера:
* принимает сообщение клиента;
* формирует ответ клиенту;
* отправляет ответ клиенту;
* имеет параметры командной строки:
  -p <port> — TCP-порт для работы (по умолчанию использует 7777);
  -a <addr> — IP-адрес для прослушивания (по умолчанию слушает все
  доступные адреса).
"""
from socket import socket, AF_INET, SOCK_STREAM
from time import time
from lib.serializers import JSONSerializer


class Server:
    """Server part of a simple messenger."""

    def __init__(self, addr: str = '', port: int = 7777, num_clients: int = 5,
                 msg_size: int = 640) -> None:
        self.addr = addr
        self.port = port
        self.num_clients = num_clients
        self.msg_size = msg_size
        self._users = {}
        self.server = None
        self._actions = {
            'presence': self.presence,
            'authenticate': self.auth,
            'msg': self.msg,
            'join': self.join,
            'leave': self.leave,
            'quit': self.quit,
        }

    @property
    def users(self):
        return self._users

    def create_user(self, user: str, password: str) -> None:
        """Create user for messaging."""

        self._users.update({user: password})

    def start(self) -> None:
        """Run messenger server."""

        s = socket(AF_INET, SOCK_STREAM)
        s.bind((self.addr, self.port))
        try:
            s.listen(self.num_clients)
        except Exception as error:
            print(error)
        else:
            print('Server started.')
            self.server = s

    def exchange_data(self) -> None:
        """Exchange data with clients."""

        session, _ = self.server.accept()
        rcv = JSONSerializer.unpack(session.recv(self.msg_size))
        print(rcv)
        action = rcv['action']
        send = self._actions[action](rcv)
        session.send(JSONSerializer.pack(send))
        session.close()

    def presence(self, *args: dict) -> dict:
        """Reply to presence-message."""

        return {"response": 200, "time": time(), "alert": "OK"}

    def auth(self, *args: dict) -> dict:
        """Reply to authentication-message."""

        user = args[0]['user']['account_name']
        password = args[0]['user']['password']
        if user in self._users and password == self._users[user]:
            return {"response": 200, "time": time(), "alert": "Authenticated"}
        elif not (user in self._users) or password != self._users[user]:
            return {"response": 402, "time": time(),
                    "error": "Wrong password or no account with that name"}

    def msg(self):
        pass

    def join(self):
        pass

    def leave(self):
        pass

    def quit(self, *args: dict) -> dict:
        """Reply to quit-message."""

        return {"response": 200, "time": time(), "alert": "OK"}


class Client:
    """Client part of a simple messenger."""
    def __init__(self, addr: str, port: int, msg_size: int = 640) -> None:
        self.addr = addr
        self.port = port
        self.msg_size = msg_size
        self.user = None
        self.password = None

    def exchange_data(self, send: dict) -> None:
        """Exchange data with server and other clients."""

        s = socket(AF_INET, SOCK_STREAM)
        try:
            s.connect((self.addr, self.port))
        except ConnectionRefusedError:
            print('Failed to establish connection with server.')
        else:
            s.send(JSONSerializer.pack(send))
            rcv = JSONSerializer.unpack(s.recv(self.msg_size))
            s.close()
            print(rcv)

    def auth(self, user: str, password: str) -> None:
        """Send authentication-request."""

        self.user = user
        self.password = password
        data = {"action": "authenticate", "time": time(),
                "user": {"account_name": self.user, "password": self.password}}
        self.exchange_data(data)

    def presence(self) -> None:
        """Send presence-message."""

        data = {"action": "presence", "time": time(), "type": "status",
                "user": {"account_name": self.user, "status": "Here"}}
        self.exchange_data(data)

    def msg(self):
        pass

    def join(self):
        pass

    def leave(self):
        pass

    def quit(self) -> None:
        """Send quit-message."""

        self.exchange_data({"action": "quit"})
