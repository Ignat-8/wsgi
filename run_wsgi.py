from framework.main import Framework
from urls import routes, fronts


def application(environ, start_response):
    """
    :param environ: словарь данных от сервера
    :param start_response: функция для ответа серверу
    """
    aplication = Framework(routes, fronts)
    return aplication(environ, start_response)
