
from import_export import resources
from import_export import  fields
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget
from .models import *


class ScheduleGroupResource(resources.ModelResource):
    """Форма для создания таблиц импорта/экспорта расписания"""
    discipline = fields.Field(column_name='Дисциплина/Преподаватель', attribute='discipline', widget=ForeignKeyWidget(TeacherDiscipline, 'name'))
    n_group = fields.Field(column_name='Номер группы', attribute='n_group', widget=ForeignKeyWidget(StudentGroup, 'number'))
    class_room = fields.Field(column_name='Номер ауд.', attribute='class_room',)
    lesson = fields.Field(column_name='Номер урока', attribute='lesson',widget=ForeignKeyWidget(NumberLesson, 'pk'))
    date = fields.Field(column_name='Дата', attribute='date',)

    class Meta:
        model = ScheduleGroup


class StudentResource(resources.ModelResource):
    """Форма для создания таблиц импорта/экспорта студента"""
    lastname = fields.Field(column_name='Фамилия', attribute='lastname', )
    firstname = fields.Field(column_name='Имя', attribute='firstname', )
    patronymic = fields.Field(column_name='Отчество', attribute='patronymic',)
    slug = fields.Field(column_name='URL студента', attribute='slug',)
    n_group = fields.Field(column_name='Номер группы', attribute='n_group', widget=ForeignKeyWidget(StudentGroup, 'number'))

    class Meta:
        model = Student

class TeachertResource(resources.ModelResource):
    """Форма для создания таблиц импорта/экспорта преподавателя"""
    lastname = fields.Field(column_name='Фамилия', attribute='lastname', )
    firstname = fields.Field(column_name='Имя', attribute='firstname', )
    patronymic = fields.Field(column_name='Отчество', attribute='patronymic',)
    slug = fields.Field(column_name='URL преподавателя', attribute='slug',)
    discipline = fields.Field(column_name='Дисциплины', attribute='discipline', widget=ManyToManyWidget(Discipline,', ','name'))

    class Meta:
        model = Teacher