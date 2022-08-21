import quopri
from datetime import datetime
from framework.requests import GetRequests, PostRequests



class Framework:
    """Класс Framework - основа фреймворка"""

    def __init__(self, routes_obj, fronts_obj):
        self.routes_lst = routes_obj
        self.fronts_lst = fronts_obj

    def __call__(self, environ, start_response):
        # получаем адрес, по которому выполнен переход
        path = environ['PATH_INFO']
        print("environ['PATH_INFO'] =", path)

        # добавление закрывающего слеша
        if not path.endswith('/'):
            path = f'{path}/'

        request = {}

        # Получаем данные запроса
        method = environ['REQUEST_METHOD']
        request['method'] = method

        if method == 'POST':
            data = PostRequests().get_request_params(environ)
            data = Framework.decode_value(data)
            request['data'] = data
            print(f'Нам пришёл post-запрос: {data}')

            data['time'] = datetime.now().strftime('%Y%m%d %H:%M:%S')
            with open(f"post_data.txt", 'a', encoding='utf-8') as file:
                file.write(str(data)+'\n')

        if method == 'GET':
            request_params = GetRequests().get_request_params(environ)
            request['request_params'] = request_params
            print(f'Нам пришли GET-параметры: {request_params}')
            if request_params:
                path = f"/curs_id/"
                request['curs_id'] = request_params['curs_id']

        print(request)  # {'method': 'GET', 'request_params': {'id': '1', 'category': '10'}}

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

    @staticmethod
    def decode_value(data):
        new_data = {}
        for k, v in data.items():
            val = bytes(v.replace('%', '=').replace("+", " "), 'UTF-8')
            val_decode_str = quopri.decodestring(val).decode('UTF-8')
            new_data[k] = val_decode_str
        return new_data
