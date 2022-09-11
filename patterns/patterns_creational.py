import copy
import quopri
from patterns.patterns_behavioral import ConsoleWriter, Subject


# Создание пользователей ==========================================================
class User:
    """абстрактный пользователь"""
    def __init__(self, name):
        self.name = name


class Teacher(User):
    """преподаватель"""
    pass


class Student(User):
    """студент"""
    def __init__(self, name):
        self.courses = []
        super().__init__(name)


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


# Создание категорий курсов =======================================================
class Category:
    # реестр
    auto_id = 0

    def __init__(self, name):
        self.id = Category.auto_id
        Category.auto_id += 1
        self.name = name
        self.courses = []
        self.subcategory = []

    def course_count(self):
        result = len(self.courses)
        for obj in self.subcategory:
            result += len(obj.courses)

        return result


# Создание курсов =================================================================
class CoursePrototype:
    """прототип курсов обучения"""
    def clone(self):
        return copy.deepcopy(self)


class Course(CoursePrototype, Subject):
    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.courses.append(self)
        self.students = []
        super().__init__()

    def __getitem__(self, item):
        return self.students[item]

    def add_student(self, student: Student):
        if student not in self.students and self not in student.courses:
            self.students.append(student)
            student.courses.append(self)
            self.notify()


class InteractiveCourse(Course):
    """Интерактивный курс"""
    pass


class RecordCourse(Course):
    """Курс в записи"""
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

    def get_student(self, name) -> Student:
        for item in self.students:
            if item.name == name:
                return item

    @staticmethod
    def decode_value(val):
        val_b = bytes(val.replace('%', '=').replace("+", " "), 'UTF-8')
        val_decode_str = quopri.decodestring(val_b)
        return val_decode_str.decode('UTF-8')
