"""
Задание на закрепление знаний по модулю yaml. Написать скрипт,
автоматизирующий сохранение данных в файле YAML-формата. Для этого:
a. Подготовить данные для записи в виде словаря, в котором первому ключу
соответствует список, второму — целое число, третьему — вложенный
словарь, где значение каждого ключа — это целое число с юникод-символом,
отсутствующим в кодировке ASCII (например, €);
b. Реализовать сохранение данных в файл формата YAML — например, в файл
file.yaml. При этом обеспечить стилизацию файла с помощью параметра
default_flow_style, а также установить возможность работы с юникодом:
allow_unicode = True;
c. Реализовать считывание данных из созданного файла и проверить,
совпадают ли они с исходными.
"""
import yaml


def write_data_to_yaml(data: dict, file_name: str) -> None:
    with open(file_name, 'w', encoding='utf-8') as file:
        yaml.dump(data, file, default_flow_style=False, allow_unicode=True)


def main():
    file = 'file.yaml'
    data = {
        'vendors': ['Cisco', 'HP', 'Dell', 'Fujitsu'],
        'site': 78,
        'devices': {
            'Cisco 2960': '\u20bd208750',
            'Cisco 3080': '\u00a37330',
            'Cisco 9200': '\u04b017540'}
    }

    write_data_to_yaml(data, file)


if __name__ == '__main__':
    main()
