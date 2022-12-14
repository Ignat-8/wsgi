from framework.templator import render
from patterns.logger import Logger
from patterns.patterns_creational import Engine
from patterns.patterns_structual import AppRoute, Debug


site = Engine()
logger = Logger('main_log')

routes = {}


@AppRoute(routes=routes, url='/')
class Index:
    """Контроллер главной страницы"""
    @Debug('index')
    def __call__(self, request):
        logger.add('start index.html')
        return '200 OK', render('index.html', 
                                data=request.get('data', None),
                                path=request.get('path', None))


@AppRoute(routes=routes, url='/curs-info/')
class CursInfo:
    """Контроллер страницы с описанием выбранного курса"""
    @Debug('curs-info')
    def __call__(self, request):
        logger.add('start curs-info.html')
        req_par = request['request_params']
        return '200 OK', render(f"curs_{req_par['curs_id']}.html", 
                                curs_id=req_par['curs_id'],
                                data=request.get('data', None))


@AppRoute(routes=routes, url='/curses/')
class Curses:
    """Контроллер страницы с курсами"""
    @Debug('curses')
    def __call__(self, request):
        logger.add('start curses.html')
        return '200 OK', render("curses.html",
                                data=request.get('data', None))


@AppRoute(routes=routes, url='/contacts/')
class About:
    """Контроллер страницы контакты"""
    @Debug('contacts')
    def __call__(self, request):
        logger.add('start contacts.html')
        return '200 OK', render('contacts.html')


@AppRoute(routes=routes, url='/admins/')
class Admins:
    """Контроллер страницы администратора"""
    @Debug('admins')
    def __call__(self, request):
        logger.add('start admins.html')
        return '200 OK', render('admins.html', objects_list=site.categories)


@AppRoute(routes=routes, url='/NotFound/')
class NotFound404:
    """Контроллер страницы 404"""
    @Debug('NotFound')
    def __call__(self, request):
        logger.add('start page_404.html')
        return '404 WHAT', render('page_404.html')


@AppRoute(routes=routes, url='/create-category/')
class CreateCategory:
    """Контроллер создания категории"""
    @Debug('create-category')
    def __call__(self, request):

        if request['method'] == 'POST':
            logger.add(f'create-category:\n{request}')
            data = request['data']
            name = data['name']
            name = site.decode_value(name)
            new_category = site.create_category(name)

            # если передан родительский объект
            if 'top_category_id' in data.keys():
                # значит создаваемый объект - это подкатегория
                new_category.is_subcategory = 1
                # в родительскую категорию сохраняем подкатегорию
                top_category = site.find_category_by_id(data['top_category_id'])
                top_category.subcategory.append(new_category)

            site.categories.append(new_category)
            # возвращаемся к списку категорий
            return '200 OK', render('admins.html', objects_list=site.categories)
        else:
            logger.add(f'create-category:\n{request}')
            if request['request_params']:
                # при создании подкатегории передается id родительской категории
                top_category_id = request['request_params']['id']
                top_category_name = request['request_params']['name']
            else:
                top_category_id = None
                top_category_name = None

            categories = site.categories
            return '200 OK', render('adm_create_category.html',
                                categories=categories,
                                top_category_id=top_category_id,
                                top_category_name = top_category_name)


@AppRoute(routes=routes, url='/courses-list/')
class CoursesList:
    """контроллер формирования списка курсов"""
    @Debug('courses-list')
    def __call__(self, request):
        logger.add('Формирование списка курсов')
        try:
            category = site.find_category_by_id(int(request['request_params']['id']))
            return '200 OK', render('curse_list.html',
                                    category=category)
        except KeyError:
            return '200 OK', 'No courses have been added yet'


@AppRoute(routes=routes, url='/create-course/')
class CreateCourse:
    """Контроллер создания курса"""
    category_id = -1

    @Debug('create-course')
    def __call__(self, request):
        logger.add(f'--- CreateCourse -----------------------------------------')
        logger.add(request)

        if request['method'] == 'POST':
            data = request['data']
            name = data['name']
            name = site.decode_value(name)

            category = None
            if self.category_id != -1:
                category = site.find_category_by_id(int(self.category_id))
                course = site.create_course('record', name, category)
                site.courses.append(course)

            return '200 OK', render('curse_list.html',
                                    category=category)
        else:
            try:
                self.category_id = int(request['request_params']['id'])
                logger.add(f'category_id: {self.category_id}')
                category = site.find_category_by_id(int(self.category_id))
                logger.add(f'category: {category}')

                return '200 OK', render('curse_create.html',
                                        category=category)
            except KeyError:
                return '200 OK', 'No categories have been added yet'


@AppRoute(routes=routes, url='/copy-course/')
class CopyCourse:
    """Контроллер копирования курса"""
    category_id = -1

    @Debug('copy-course')
    def __call__(self, request):
        logger.add(f'--- CopyCourse ------------------------------------------------------------')
        logger.add(request)

        if request['method'] == 'POST':
            data = request['data']
            name = data['name']
            name = site.decode_value(name)

            category = None
            if self.category_id != -1:
                category = site.find_category_by_id(int(self.category_id))

                course = site.create_course('record', name, category)
                site.courses.append(course)
            
            return '200 OK', render('curse_list.html',
                                    category=category)
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
            category = new_course.category

            logger.add(f'Успешное копирование курса, {new_course}')
            return '200 OK', render('curse_create.html', category=category)
