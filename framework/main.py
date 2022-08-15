# import quopri
# from pprint import pprint


class Framework:
    """Класс Framework - основа фреймворка"""

    def __init__(self, routes_obj, fronts_obj):
        self.routes_lst = routes_obj
        self.fronts_lst = fronts_obj

    def __call__(self, environ, start_response):
        # получаем адрес, по которому выполнен переход
        path = environ['PATH_INFO']
        print("environ['PATH_INFO'] =", path)

        query_string = environ['QUERY_STRING']
        print(f"query_string ='{query_string}'")  # -> 'id=1&category=10'

        request_params = self.parse_input_data(query_string)
        print("request_params =", request_params)  # -> {'id': '1', 'category': '10'}

        if request_params:
            path = f'/curs_id/'
            request = request_params
        else:
            request = {}

        # добавление закрывающего слеша
        if not path.endswith('/'):
            path = f'{path}/'

        # находим нужный view контроллер
        if path in self.routes_lst:
            view = self.routes_lst[path]
        else:
            view = self.routes_lst['NotFound']

        # наполняем словарь request элементами
        # этот словарь получат все контроллеры
        # отработка паттерна front controller
        for front in self.fronts_lst:
            front(request)
        
        # запуск контроллера с передачей объекта request
        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]

    def parse_input_data(self, data):
        result = {}

        if data:
            params = data.split('&')
            for item in params:
                k, v = item.split('=')
                result[k] = v

        return result

    # @staticmethod
    # def decode_value(data):
    #     new_data = {}
    #     for k, v in data.items():
    #         val = bytes(v.replace('%', '=').replace("+", " "), 'UTF-8')
    #         val_decode_str = quopri.decodestring(val).decode('UTF-8')
    #         new_data[k] = val_decode_str
    #     return new_data
