from django.contrib import admin
from .models import *
from import_export.admin import ImportExportActionModelAdmin
from import_export import resources
from import_export import  fields
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget


class StudentAdmin(admin.ModelAdmin):
    list_display = ('lastname', 'firstname', 'patronymic', 'n_group', )
    list_display_links = ('lastname', )
    search_fields = ('lastname', 'firstname', 'patronymic', )
    list_filter = ('n_group', )
    prepopulated_fields = {'slug': ('lastname', 'firstname', 'patronymic')}


class Disciplineship(admin.TabularInline):
    model = Teacher.discipline.through


class TeacherAdmin(admin.ModelAdmin):
    list_display = ('lastname', 'firstname', 'patronymic', )
    list_display_links = ('lastname',  )
    search_fields = ('lastname', 'firstname', 'patronymic', )
    list_filter = ('discipline', )
    prepopulated_fields = {'slug': ('lastname', 'firstname', 'patronymic',)}
    inlines = [Disciplineship, ]
    exclude = ('discipline',)


class DisciplineAdmin(admin.ModelAdmin):
    inlines = [Disciplineship, ]


class ScheduleGroupInTabular(admin.TabularInline):
    model = ScheduleGroup
    extra = 6


class ScheduleGroupResource(resources.ModelResource):
    discipline = fields.Field(column_name='Дисциплина/Преподаватель', attribute='discipline', widget=ForeignKeyWidget(TeacherDiscipline, 'name'))
    n_group = fields.Field(column_name='Номер группы', attribute='n_group', widget=ForeignKeyWidget(StudentGroup, 'number'))
    class_room = fields.Field(column_name='Номер ауд.', attribute='class_room',)
    lesson = fields.Field(column_name='Номер урока', attribute='lesson',widget=ForeignKeyWidget(NumberLesson, 'pk'))
    date = fields.Field(column_name='Дата', attribute='date',)
    class Meta:
        model = ScheduleGroup


class ScheduleGroupAdmin(ImportExportActionModelAdmin):
    resource_class = ScheduleGroupResource
    list_display = ['date', 'discipline', 'n_group', 'lesson', 'class_room']


class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_at', 'published_for_parents', 'published_for_teacher' )
    list_display_links = ('title', )
    search_fields = ('title', )
    list_editable = ('published_for_parents', 'published_for_teacher')
    list_filter = ('published_at', 'published_for_parents', 'published_for_teacher' )
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Student, StudentAdmin)
admin.site.register(StudentGroup,)
admin.site.register(ScheduleGroup,ScheduleGroupAdmin)
admin.site.register(Teacher, TeacherAdmin)
#admin.site.register(NumberLesson)
#admin.site.register(Weekday)
admin.site.register(Discipline, DisciplineAdmin)
admin.site.register(News, NewsAdmin)
#admin.site.register(Mark)



