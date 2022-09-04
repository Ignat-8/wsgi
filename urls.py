import os
from views import logger


# front controller
def secret_front(request):
    logger.add('формируем secret_front')


def other_front(request):
    logger.add('формируем other_front')
    request['path'] = os.getcwd()


fronts = [secret_front, other_front]

# routes = {
#     '/': Index(),
#     '/contacts/': About(),
#     '/curses/': Curses(),
#     '/curs-info/': Curs(),

#     '/create-category/': CreateCategory(),
#     '/courses-list/': CoursesList(),
#     '/create-course/': CreateCourse(),
#     '/copy-course/': CopyCourse(),
    
    
#     '/admins/': Admins(),
#     'NotFound': NotFound404(),
# }
