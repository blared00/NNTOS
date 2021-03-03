from django.contrib import admin
from .models import *


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


class StudentGroupAdmin(admin.ModelAdmin):
    inlines = [ScheduleGroupInTabular, ]

class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_at', 'published_for_parents', 'published_for_teacher' )
    list_display_links = ('title',  )
    search_fields = ('title', )
    list_editable = ('published_for_parents', 'published_for_teacher')
    list_filter = ('published_at', 'published_for_parents', 'published_for_teacher' )
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Student, StudentAdmin)
admin.site.register(StudentGroup, StudentGroupAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(NumberLesson)
admin.site.register(Weekday)
admin.site.register(Discipline,DisciplineAdmin)
admin.site.register(News, NewsAdmin)




