"""
Задание на закрепление знаний по модулю CSV. Написать скрипт,
осуществляющий выборку определенных данных из файлов info_1.txt,
info_2.txt, info_3.txt и формирующий новый «отчетный» файл в формате
CSV. Для этого:
a. Создать функцию get_data(), в которой в цикле осуществляется перебор
файлов с данными, их открытие и считывание данных. В этой функции из
считанных данных необходимо с помощью регулярных выражений извлечь
значения параметров «Изготовитель системы»,  «Название ОС», «Код
продукта», «Тип системы». Значения каждого параметра поместить в
соответствующий список. Должно получиться четыре списка — например,
os_prod_list, os_name_list, os_code_list, os_type_list. В этой же
функции создать главный список для хранения данных отчета — например,
main_data — и поместить в него названия столбцов отчета в виде списка:
«Изготовитель системы», «Название ОС», «Код продукта», «Тип системы».
Значения для этих столбцов также оформить в виде списка и поместить в
список main_data (также для каждого файла);
b. Создать функцию write_to_csv(), в которую передавать ссылку на
CSV-файл. В этой функции реализовать получение данных через вызов
функции get_data(), а также сохранение подготовленных данных в
соответствующий CSV-файл;
c. Проверить работу программы через вызов функции write_to_csv().
"""
import os.path as path
import re
import csv


def get_data() -> list:
    files = ('info_1.txt', 'info_2.txt', 'info_3.txt')
    headers = ['Изготовитель системы', 'Название ОС', 'Код продукта',
               'Тип системы']
    os_prod_list, os_name_list, os_code_list, os_type_list = ([] for _ in
                                                              range(4))
    main_data = [headers, os_prod_list, os_name_list, os_code_list,
                 os_type_list]

    for file_name in files:
        with open(path.join('src', file_name), encoding='cp1251') as file:
            data = file.read()
            # for i in range(len(headers)):
            #     main_data[i + 1].extend(
            #         re.findall(fr'{headers[i]}:\s*(.+)\n', data))
            os_prod_list.extend(re.findall(fr'{headers[0]}:\s*(.+)\n', data))
            os_name_list.extend(re.findall(fr'{headers[1]}:\s*(.+)\n', data))
            os_code_list.extend(re.findall(fr'{headers[2]}:\s*(.+)\n', data))
            os_type_list.extend(re.findall(fr'{headers[3]}:\s*(.+)\n', data))
    return main_data


def write_to_csv(file_name: str, data: list) -> None:
    with open(file_name, 'w') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC)
        writer.writerows(data)


def main():
    csv_file = 'result.csv'

    write_to_csv(csv_file, get_data())


if __name__ == '__main__':
    main()
