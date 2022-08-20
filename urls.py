import os
from datetime import date
from views import Index, About, NotFound404


# front controller
def secret_front(request):
    request['data'] = date.today()


def other_front(request):
    request['path'] = os.getcwd()


fronts = [secret_front, other_front]

routes = {
    '/': Index(),
    '/about/': About(),
    'NotFound': NotFound404(),
}
