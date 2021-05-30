"""
Создать текстовый файл test_file.txt, заполнить его тремя строками:
«сетевое программирование», «сокет», «декоратор». Проверить кодировку
файла по умолчанию. Принудительно открыть файл в формате Unicode и
вывести его содержимое.
"""


def main() -> None:
    lines = ('сетевое программирование\n', 'сокет\n', 'декоратор\n')

    with open('data.txt', 'w') as file:
        file.writelines(lines)
        print(f'Default encoding of the file {file.name} is {file.encoding}.')

    with open('data.txt', 'r', encoding='utf-8') as file:
        try:
            print(file.read())
        except UnicodeDecodeError:
            print('Cannot translate this file in Unicode.')


if __name__ == '__main__':
    main()
