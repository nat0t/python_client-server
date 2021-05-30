"""
Определить, какие из слов «attribute», «класс», «функция», «type»
невозможно записать в байтовом типе.
"""


def main() -> None:
    words = ('attribute', 'класс', 'функция', 'type')

    for word in words:
        try:
            bytes(word, 'ascii')
        except UnicodeEncodeError:
            print(f'Word "{word}" cannot be written as bytes.')


if __name__ == '__main__':
    main()
