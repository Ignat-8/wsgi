import os
from datetime import datetime


PATH = os.path.dirname(os.path.abspath(__file__))
now = f'{datetime.now().strftime("%Y%m%d")}'

# порождающий паттерн Синглтон
class SingletonByName(type):

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class Logger(metaclass=SingletonByName):

    def __init__(self, name):
        self.name = name

    def log(self, text):
        print(f'log {self.name} --->', text)
        with open(f'{now}_{self.name}.txt', 'a', encoding='utf-8') as logfile:
            logfile.write(f'{datetime.now().strftime("%Y%m%d %H:%M:%S")}: {text}\n')


if __name__== '__main__':
    print('start logger')
    logger1 = Logger('log1')
    logger2 = Logger('log2')

    logger1.log('some text1')
    logger2.log('some text2')
