"""
Задание на закрепление знаний по модулю json. Есть файл orders в формате
JSON с информацией о заказах. Написать скрипт, автоматизирующий его
заполнение данными. Для этого:
a. Создать функцию write_order_to_json(), в которую передается 5
параметров — товар (item), количество (quantity), цена (price),
покупатель (buyer), дата (date). Функция должна предусматривать запись
данных в виде словаря в файл orders.json. При записи данных указать
величину отступа в 4 пробельных символа;
b. Проверить работу программы через вызов функции write_order_to_json()
с передачей в нее значений каждого параметра.
"""
import os.path as path
import json


def write_order_to_json(item: str, quantity: int, price: int, buyer: str,
                        date: str) -> None:
    file_name = 'orders.json'
    to_json = {'orders': []}
    order = {
        "item": item,
        "quantity": quantity,
        "price": price,
        "buyer": buyer,
        "date": date
    }

    to_json['orders'].append(order)
    with open(path.join('src', file_name), 'w', encoding='cp1251') as file:
        json.dump(to_json, file, indent=4)


def main():
    write_order_to_json('RTX 3080', 10, 250000, 'Vasya Miner', '30.05.2021')


if __name__ == '__main__':
    main()
