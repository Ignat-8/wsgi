from framework.templator import render
from patterns.logger import Logger
from patterns.patterns import Engine


site = Engine()
logger = Logger('main_log')


class Index:
    def __call__(self, request):
        logger.add('start index.html')
        return '200 OK', render('index.html', 
                                data=request.get('data', None),
                                path=request.get('path', None))


class Curs:
    def __call__(self, request):
        logger.add('start curs_id.html')
        return '200 OK', render(f"curs_{request['curs_id']}.html", 
                                curs_id=request['curs_id'],
                                data=request.get('data', None))


class Curses:
    def __call__(self, request):
        logger.add('start curses.html')
        return '200 OK', render("curses.html",
                                data=request.get('data', None))


class About:
    def __call__(self, request):
        logger.add('start contacts.html')
        return '200 OK', render('contacts.html')


class Admins:
    def __call__(self, request):
        logger.add('start admins.html')
        return '200 OK', render('admins.html', objects_list=site.categories)


class NotFound404:
    def __call__(self, request):
        logger.add('start page_404.html')
        return '404 WHAT', render('page_404.html')


# контроллер - создать категорию
class CreateCategory:
    def __call__(self, request):

        if request['method'] == 'POST':
            # метод пост
            logger.add(f'POST:\n{request}')
            data = request['data']
            name = data['name']
            name = site.decode_value(name)

            new_category = site.create_category(name)
            site.categories.append(new_category)
            # возвращаемся к списку категорий
            return '200 OK', render('admins.html', objects_list=site.categories)
        else:
            categories = site.categories
            return '200 OK', render('adm_create_category.html', categories=categories)


class CoursesList:
    """контроллер - список курсов"""
    def __call__(self, request):
        logger.add('Формирование списка курсов')
        try:
            category = site.find_category_by_id(int(request['request_params']['id']))
            return '200 OK', render('curse_list.html',
                                    objects_list=category.courses,
                                    name=category.name,
                                    id=category.id)
        except KeyError:
            return '200 OK', 'No courses have been added yet'


# контроллер - создать курс
class CreateCourse:
    category_id = -1

    def __call__(self, request):
        if request['method'] == 'POST':
            logger.add(f'--- CreateCourse, metod POST -----------------------------------------')
            # метод пост
            data = request['data']
            name = data['name']
            name = site.decode_value(name)

            category = None
            if self.category_id != -1:
                category = site.find_category_by_id(int(self.category_id))
                course = site.create_course('record', name, category)
                site.courses.append(course)

            logger.add(f'---------------------------------------------------------------------')
            return '200 OK', render('curse_list.html',
                                    objects_list=category.courses,
                                    name=category.name,
                                    id=category.id)
        else:
            try:
                logger.add(f'--- CreateCourse, metod GET -----------------------------------------')
                self.category_id = int(request['request_params']['id'])
                logger.add(f'category_id: {self.category_id}')
                category = site.find_category_by_id(int(self.category_id))
                logger.add(f'category: {category}')
                logger.add(f'--------------------------------------------------------------------')
                return '200 OK', render('curse_create.html',
                                        objects_list=category.courses,
                                        name=category.name,
                                        id=category.id)
            except KeyError:
                return '200 OK', 'No categories have been added yet'


# контроллер - копировать курс
class CopyCourse:
    category_id = -1

    def __call__(self, request):
        logger.add(f'--- CopyCourse ------------------------------------------------------------')
        logger.add(f"method : {request['method']}")

        if request['method'] == 'POST':
            data = request['data']
            name = data['name']
            name = site.decode_value(name)

            category = None
            if self.category_id != -1:
                category = site.find_category_by_id(int(self.category_id))

                course = site.create_course('record', name, category)
                site.courses.append(course)
            logger.add(f'---------------------------------------------------------------------')
            return '200 OK', render('curse_list.html',
                                    objects_list=category.courses,
                                    name=category.name,
                                    id=category.id)
        else:
            request_params = request['request_params']
            name = request_params['name']
            name = site.decode_value(name)
            old_course = site.get_course(name)
            new_name = f'copy_{name}'
            new_course = old_course.clone()
            new_course.name = new_name
            site.courses.append(new_course)
            self.category_id = int(new_course.category.id)

            logger.add(f'Успешное копирование курса, {new_course}')
            return '200 OK', render('curse_create.html', objects_list=new_course)
