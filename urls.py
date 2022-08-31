import os
from datetime import date
from views import (Index, About, Curs, Curses,
                   CoursesList, CreateCourse, CopyCourse, CreateCategory,
                   NotFound404, Admins, logger)


# front controller
def secret_front(request):
    logger.add('формируем secret_front')
    # request['data'] = date.today()


def other_front(request):
    logger.add('формируем other_front')
    request['path'] = os.getcwd()


fronts = [secret_front, other_front]

routes = {
    '/': Index(),
    '/contacts/': About(),
    '/curses/': Curses(),
    '/curs-info/': Curs(),

    '/create-category/': CreateCategory(),
    '/courses-list/': CoursesList(),
    '/create-course/': CreateCourse(),
    '/copy-course/': CopyCourse(),
    
    
    '/admins/': Admins(),
    'NotFound': NotFound404(),
}
