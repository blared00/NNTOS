from django.contrib import admin
from .models import *
from import_export.admin import ImportExportActionModelAdmin
from .resources import ScheduleGroupResource, StudentResource, TeachertResource
"""Визуализация БД  для админ.панели (создание/редактирование объектов БД)"""


class StudentAdmin(ImportExportActionModelAdmin):
    """Таблица студентов"""
    resource_class = StudentResource
    list_display = ('lastname', 'firstname', 'patronymic', 'n_group', )
    list_display_links = ('lastname', )
    search_fields = ('lastname', 'firstname', 'patronymic', )
    list_filter = ('n_group', )
    prepopulated_fields = {'slug': ('lastname', 'firstname', 'patronymic')}


class Disciplineship(admin.TabularInline):
    """Форма для отображения дисциплин при создании/редактировании учителя"""
    model = Teacher.discipline.through


class TeacherAdmin(ImportExportActionModelAdmin):
    """Таблица преподавателей"""
    resource_class = TeachertResource
    list_display = ('lastname', 'firstname', 'patronymic', )
    list_display_links = ('lastname',  )
    search_fields = ('lastname', 'firstname', 'patronymic', )
    list_filter = ('discipline', )
    prepopulated_fields = {'slug': ('lastname', 'firstname', 'patronymic',)}
    inlines = [Disciplineship, ]
    exclude = ('discipline',)


class DisciplineAdmin(admin.ModelAdmin):
    """Таблица дисциплин"""
    inlines = [Disciplineship, ]


class ScheduleGroupInTabular(admin.TabularInline):
    """Форма отображения пар при создании/редактировании группы"""
    model = ScheduleGroup
    extra = 6


class StudentGroupAdmin(admin.ModelAdmin):
    """Таблица групп"""
    inlines = [ScheduleGroupInTabular, ]


class ScheduleGroupAdmin(ImportExportActionModelAdmin):
    """Таблица расписания"""
    resource_class = ScheduleGroupResource
    list_display = ['date', 'discipline', 'n_group', 'lesson', 'class_room']
    list_filter = ('discipline','n_group', 'date',)


class NewsAdmin(admin.ModelAdmin):
    """Таблица новостей"""
    list_display = ('title', 'published_at', 'published_for_parents', 'published_for_teacher' )
    list_display_links = ('title', )
    search_fields = ('title', )
    list_editable = ('published_for_parents', 'published_for_teacher')
    list_filter = ('published_at', 'published_for_parents', 'published_for_teacher' )
    prepopulated_fields = {'slug': ('title',)}


"""Список отображаемых таблиц в админ.панели"""
admin.site.register(Student, StudentAdmin)
admin.site.register(StudentGroup,StudentGroupAdmin)
admin.site.register(ScheduleGroup,ScheduleGroupAdmin)
admin.site.register(Teacher, TeacherAdmin)
#admin.site.register(NumberLesson)
#admin.site.register(Weekday)
admin.site.register(Discipline, DisciplineAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Mark)



