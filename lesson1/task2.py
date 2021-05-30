"""
Каждое из слов «class», «function», «method» записать в байтовом типе
без преобразования в последовательность кодов (не используя методы
encode и decode) и определить тип, содержимое и длину соответствующих
переменных.
"""


def main() -> None:
    columns = 15

    headers = ('Word', 'Type', 'Value', 'Length')
    words = ('class', 'function', 'method')
    for header in headers:
        print(f'{header:^{columns}}', end='')
    print()
    for word in words:
        bword = bytes(word, 'utf-8', 'replace')
        print(
            f'{word:^{columns}}{str(type(bword)):^{columns}}'
            f'{str(bword):^{columns}}{len(bword):^{columns}}')


if __name__ == '__main__':
    main()
