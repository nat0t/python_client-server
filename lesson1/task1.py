"""
Каждое из слов «разработка», «сокет», «декоратор» представить в
строковом формате и проверить тип и содержание соответствующих
переменных. Затем с помощью онлайн-конвертера преобразовать строковые
представление в формат Unicode и также проверить тип и содержимое
переменных.
"""


def main() -> None:
    words = (('разработка',
              b'\xd1\x80\xd0\xb0\xd0\xb7\xd1\x80\xd0\xb0\xd0\xb1\xd0\xbe\xd1\x82\xd0\xba\xd0\xb0'),
             ('сокет',
              b'\xd1\x81\xd0\xbe\xd0\xba\xd0\xb5\xd1\x82'),
             ('декоратор',
              b'\xd0\xb4\xd0\xb5\xd0\xba\xd0\xbe\xd1\x80\xd0\xb0\xd1\x82\xd0\xbe\xd1\x80'))

    for word in words:
        print(
            f'Word:         {word[0]}\nType:         {type(word[0])}\n'
            f'Word (UTF-8): {word[1]}\nType (UTF-8): {type(word[1])}')
        print('-' * 100)


if __name__ == '__main__':
    main()
