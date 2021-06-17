"""
1. Продолжая задачу логирования, реализовать декоратор @log, фиксирующий
обращение к декорируемой функции. Он сохраняет ее имя и аргументы.
2. В декораторе @log реализовать фиксацию функции, из которой была
вызвана декорированная. Если имеется такой код:
@log
    def func_z():
        pass
    def main():
        func_z()
...в логе должна быть отражена информация:
"<дата-время> Функция func_z() вызвана из функции main"
"""
from functools import wraps
import logging.config
from inspect import currentframe, getouterframes

logging.config.fileConfig('logging.ini')
logger = logging.getLogger('messenger.call')


def log(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        caller = getouterframes(currentframe())[1][3]
        logger.info(
            f'Function {func.__name__} was called with args {args},'
            f'{kwargs}. This one was called from {caller}.')
        return func(*args, **kwargs)
    return wrapper
