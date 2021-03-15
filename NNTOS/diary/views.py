from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import *
# Create your views here.


class ParentsView(View):
    def get(self, request, student_name):
        ''' Получение предметов студента и отображение расписания'''
        student = get_object_or_404(Student, slug=student_name)
        schedule = {}
        weekdays = Weekday.objects.all()
        weekdays_n = [0, 3, 1, 4, 2, 5]

        for n in range(0, 6):
            weekdays_n[n] = weekdays[weekdays_n[n]]
        for weekday in weekdays_n:
            a = ['', '', '', '', '', '']
            lessons = weekday.schedulegroup_set.filter(n_group=student.n_group)
            for n in range(0, 6):
                for l in lessons:
                    if l.lesson.pk == n+1:
                        a[n]=l
            schedule[weekday] = a
        print(schedule)
        ''' Отображение новстей и пагинация'''
        order_news = request.GET.get('sorting')
        #if order_news == 'last':
        #    news = News.objects.filter(published_for_parents=True).order_by('published_at')
        #else:
        menu = {'#glavnaya': 'Главная',
                '#dosca': 'Доска объявлений',
                '#dnevnik': 'Электронный дневник',
                '#uved': 'Уведомления'
                }
        news = News.objects.filter(published_for_parents=True)
        paginator_news = Paginator(news, 5)
        page_number = request.GET.get('page')
        page_obj = paginator_news.get_page(page_number)
        return render(request, 'index_perents.html', context={'student': student,
                                                              'menu': menu.items(),
                                                              'schedule': schedule.items(),
                                                              'title': f'Дневник|{student}',
                                                              'chet': [2, 4, 6],
                                                              'news': page_obj,
                                                              })


class TeacherView(View):
    def get(self, request, teacher_name):
        teacher = get_object_or_404(Teacher, slug=teacher_name)
        schedule = {}
        weekdays_t = Weekday.objects.all()
        weekdays_n = [0, 3, 1, 4, 2, 5]

        for n in range(0, 6):
            weekdays_n[n] = weekdays_t[weekdays_n[n]]
        for weekday in weekdays_t:
            a = ['', '', '', '', '', '']

            lessons = weekday.schedulegroup_set.filter(discipline__teacher=teacher)
            for n in range(0, 6):
                for l in lessons:
                    if l.lesson.pk == n+1:
                        a[n]=l
            schedule[weekday] = a

        '''Представление расписания в постраничную форму
        if request.GET.get('wd'):
            weekday_get = request.GET.get('wd')
            schedule_w = get_object_or_404(Weekday, name=weekday_get)
        else:
            weekday_get = 'Понедельник'
            schedule_w = Weekday.objects.get(name=weekday_get)'''
        menu = {'#glavnaya': 'Главная',
                '#dosca': 'Доска объявлений',
                '#schedule_teacher': 'Расписание',
                '#journal': 'Электронный журнал'
                }
        news = News.objects.filter(published_for_teacher=True)
        paginator_news = Paginator(news, 1)
        page_number = request.GET.get('page')
        page_obj = paginator_news.get_page(page_number)
        return render(request, 'index_teach.html', context={'teacher': teacher,
                                                            'menu': menu.items(),
                                                            'title': f'Журнал|{teacher}',
                                                            'news': page_obj,
                                                            'schedule': schedule[schedule_w],
                                                            'weekdays': weekdays_list.items(),
                                                            'weekday_get': weekday_get})


class LoginView(View):
    def get(self, request):
        return render(request, 'login_form.html')


class NewsView(View):
    def get(self, request, news_slug):
        news_information = get_object_or_404(News, slug=news_slug)
        return HttpResponse(f'Здесь объявление {news_information}')
