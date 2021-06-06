import argparse
from lib.main import Server


def main():
    parser = argparse.ArgumentParser(description='Messenger startup settings')
    parser.add_argument('-a', action='store', dest='addr', default='',
                        help='Listening address')
    parser.add_argument('-p', action='store', dest='port', default=7777,
                        help='Listening port')
    args = parser.parse_args()

    server = Server(addr=args.addr, port=int(args.port))
    server.create_user('Kolya', 'Admin')
    server.start()
    while True:
        server.exchange_data()


if __name__ == '__main__':
    main()
