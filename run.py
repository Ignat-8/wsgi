from wsgiref.simple_server import make_server

from framework.main import Framework, DebugApplication, FakeApplication
from urls import fronts
from views import logger, routes


application = Framework(routes, fronts)
# application = DebugApplication(routes, fronts)
# application = FakeApplication(routes, fronts)

with make_server('', 8081, application) as httpd:
    logger.add("Запуск сервера на порту 8081...")
    httpd.serve_forever()
