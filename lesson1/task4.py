"""
Преобразовать слова «разработка», «администрирование», «protocol»,
«standard» из строкового представления в байтовое и выполнить обратное
преобразование (используя методы encode и decode).
"""


def main() -> None:
    words = ('разработка', 'администрирование', 'protocol', 'standard')

    for word in words:
        word.encode('utf-8').decode('utf-8')


if __name__ == '__main__':
    main()
