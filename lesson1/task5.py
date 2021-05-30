"""
Выполнить пинг веб-ресурсов yandex.ru, youtube.com и преобразовать
результаты из байтовового в строковый тип на кириллице.
"""
import platform
import subprocess


def ping(host: str, packets: int) -> None:
    option = '-n' if platform.system().lower() == 'windows' else '-c'
    encoding = 'cp866' if platform.system().lower() == 'windows' else 'utf-8'

    command = ('ping', option, str(packets), host)
    ping_result = subprocess.Popen(command, stdout=subprocess.PIPE)

    for line in ping_result.stdout:
        print(line.decode(encoding).strip())


if __name__ == '__main__':
    PACKETS = 2
    TARGETS = ('yandex.ru', 'youtube.com')
    for target in TARGETS:
        ping(target, PACKETS)
