import argparse
from lib.main import Client


def main():
    parser = argparse.ArgumentParser(description='Messenger startup settings')
    parser.add_argument('addr', help='Server address')
    parser.add_argument('port', help='Server port')
    args = parser.parse_args()

    client = Client(addr=args.addr, port=int(args.port))
    client.auth('Vasya', 'Miner')
    client.auth('Kolya', 'Admin')
    client.presence()
    client.quit()


if __name__ == '__main__':
    main()
