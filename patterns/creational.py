import copy
import quopri
import sqlite3
from patterns.behavioral import ConsoleWriter, Subject
from patterns.unit_of_work import DomainObject


# Создание пользователей ==========================================================
class User:
    """абстрактный пользователь"""
    def __init__(self, name):
        self.name = name


class Teacher(User):
    """преподаватель"""
    pass


class Student(User, DomainObject):
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
    def create(cls, type_, name):
        return cls.types[type_](name)


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
    def create_user(type_, name):
        return UserFactory.create(type_, name)

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


class StudentMapper:

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = 'student'

    def all(self):
        statement = f'SELECT * from {self.tablename}'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id, name = item
            student = Student(name)
            student.id = id
            result.append(student)
        return result

    def find_by_id(self, id):
        statement = f"SELECT id, name FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            return Student(*result)
        else:
            raise RecordNotFoundException(f'record with id={id} not found')

    def insert(self, obj):
        statement = f"INSERT INTO {self.tablename} (name) VALUES (?)"
        self.cursor.execute(statement, (obj.name,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, obj):
        statement = f"UPDATE {self.tablename} SET name=? WHERE id=?"
        # Где взять obj.id? Добавить в DomainModel? Или добавить когда берем объект из базы
        self.cursor.execute(statement, (obj.name, obj.id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, obj):
        statement = f"DELETE FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


connection = sqlite3.connect('framework_db.sqlite')


# архитектурный системный паттерн - Data Mapper
class MapperRegistry:
    mappers = {
        'student': StudentMapper,
        #'category': CategoryMapper
    }

    @staticmethod
    def get_mapper(obj):
        if isinstance(obj, Student):
            return StudentMapper(connection)

        #if isinstance(obj, Category):
            #return CategoryMapper(connection)

    @staticmethod
    def get_current_mapper(name):
        return MapperRegistry.mappers[name](connection)


class DbCommitException(Exception):
    def __init__(self, message):
        super().__init__(f'Db commit error: {message}')


class DbUpdateException(Exception):
    def __init__(self, message):
        super().__init__(f'Db update error: {message}')


class DbDeleteException(Exception):
    def __init__(self, message):
        super().__init__(f'Db delete error: {message}')


class RecordNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(f'Record not found: {message}')

