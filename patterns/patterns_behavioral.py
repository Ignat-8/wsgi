import jsonpickle
import quopri
from framework.templator import render


class Observer:
    """поведенческий паттерн - наблюдатель"""
    def update(self, subject):
        pass


class Subject:

    def __init__(self):
        self.observers = []

    def notify(self):
        for item in self.observers:
            item.update(self)


class SmsNotifier(Observer):
    """Контроллер оповещения по смс"""
    def update(self, subject):
        print('SMS->', 'к нам присоединился', subject.students[-1].name)


class EmailNotifier(Observer):
    """Контроллер оповещения по email"""
    def update(self, subject):
        print('EMAIL->', 'к нам присоединился', subject.students[-1].name)


class BaseSerializer:
    """Контрллер преобразования данных в json формат"""
    def __init__(self, obj):
        self.obj = obj

    def save(self):
        return jsonpickle.dumps(self.obj)

    @staticmethod
    def load(data):
        return jsonpickle.loads(data)


class TemplateView:
    """поведенческий паттерн - Шаблонный метод"""
    template_name = 'template.html'

    def get_context_data(self):
        return {}

    def get_template(self):
        return self.template_name

    def render_template_with_context(self, name, is_conflict=0):
        template_name = self.get_template()
        context = self.get_context_data()
        context['is_conflict'] = is_conflict
        context['name'] = name
        print('TemplateView context:\n', context)

        if not is_conflict:    
            return '200 OK', render(template_name, **context)
        else:
            return '409 Conflict', render(template_name, **context)

    def __call__(self, request):
        name = ''
        return self.render_template_with_context(name)


class ListView(TemplateView):
    queryset = []
    template_name = 'list.html'
    context_object_name = 'objects_list'

    def get_queryset(self):
        print(self.queryset)
        return self.queryset

    def get_context_object_name(self):
        return self.context_object_name

    def get_context_data(self):
        queryset = self.get_queryset()
        context_object_name = self.get_context_object_name()
        context = {context_object_name: queryset}
        return context


class CreateView(TemplateView):
    template_name = 'create.html'

    @staticmethod
    def get_request_data(request):
        return request['data']

    def create_obj(self, data):
        pass
    
    def duble_obj_name(self, name):
        pass

    def decode_value(self, val):
        val_b = bytes(val.replace('%', '=').replace("+", " "), 'UTF-8')
        val_decode_str = quopri.decodestring(val_b)
        return val_decode_str.decode('UTF-8')

    def __call__(self, request):
        if request['method'] == 'POST':
            data = self.get_request_data(request)
            name = data['name']
            name = self.decode_value(name)

            if not self.duble_obj_name(name):
                self.create_obj(data)
                is_conflict = 0
                return self.render_template_with_context(is_conflict)
            else:
                is_conflict = 1
                return self.render_template_with_context(name, is_conflict)
        else:
            return super().__call__(request)


class ConsoleWriter:
    """поведенческий паттерн - Стратегия"""
    def write(self, text):
        print(text)


class FileWriter:
    """Контроллер записи в файл"""
    def __init__(self, file_name):
        self.file_name = file_name

    def write(self, text):
        with open(self.file_name, 'a', encoding='utf-8') as f:
            f.write(f'{text}\n')
