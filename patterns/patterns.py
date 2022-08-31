import copy
import quopri


# Создание категорий курсов =======================================================
class Category:
    # реестр
    auto_id = 0

    def __init__(self, name):
        self.id = Category.auto_id
        Category.auto_id += 1
        self.name = name
        self.courses = []

    def course_count(self):
        result = len(self.courses)
        # if self.name:
        #     result += self.name.course_count()
        return result


# Создание курсов =================================================================
class CoursePrototype:
    """прототип курсов обучения"""
    def clone(self):
        return copy.deepcopy(self)


class Course(CoursePrototype):
    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.courses.append(self)


# Интерактивный курс
class InteractiveCourse(Course):
    pass


# Курс в записи
class RecordCourse(Course):
    pass


class CourseFactory:
    """порождающий паттерн Абстрактная фабрика - фабрика курсов"""
    types = {
        'interactive': InteractiveCourse,
        'record': RecordCourse
    }

    # порождающий паттерн Фабричный метод
    @classmethod
    def create(cls, type_, name, category):
        return cls.types[type_](name, category)


# Создание пользователей ==========================================================
class User:
    """абстрактный пользователь"""
    pass


class Teacher(User):
    """преподаватель"""
    pass


class Student(User):
    """студент"""
    pass


class UserFactory:
    """порождающий паттерн Абстрактная фабрика
        - фабрика пользователей"""
    types = {
        'student': Student,
        'teacher': Teacher
    }

    # порождающий паттерн Фабричный метод
    @classmethod
    def create(cls, type_):
        return cls.types[type_]()


# Основной интерфейс проекта ======================================================
class Engine:
    def __init__(self):
        self.teachers = []
        self.students = []
        self.courses = []
        self.categories = []

    @staticmethod
    def create_user(type_):
        return UserFactory.create(type_)

    @staticmethod
    def create_category(name):
        return Category(name)

    def find_category_by_id(self, id):
        for item in self.categories:
            if int(item.id) == int(id):
                print('item.id =', item.id, ', id =', id, ', item.name=', item.name)
                return item
        raise Exception(f'Нет категории с id = {id}')

    @staticmethod
    def create_course(type_, name, category):
        return CourseFactory.create(type_, name, category)

    def get_course(self, name):
        for item in self.courses:
            if item.name == name:
                return item
        return None

    @staticmethod
    def decode_value(val):
        val_b = bytes(val.replace('%', '=').replace("+", " "), 'UTF-8')
        val_decode_str = quopri.decodestring(val_b)
        return val_decode_str.decode('UTF-8')
