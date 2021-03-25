from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from .form import LoginForm
from .models import *
# Create your views here.


class ParentsView(View):
    def dispatch(self, request, student_name):
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

        ''' Отображение новостей и пагинация'''
        news = News.objects.filter(published_for_parents=True)
        order_news = request.POST.get('sorting_news', 'first')
        if order_news == 'last':
            news = News.objects.filter(published_for_parents=True).order_by('published_at')

        print(order_news)

        menu = {'#glavnaya': 'Главная',
                '#dosca': 'Доска объявлений',
                '#dnevnik': 'Электронный дневник',
                '#uved': 'Уведомления'
                }

        paginator_news = Paginator(news, 5)
        page_number = request.GET.get('page')
        page_obj = paginator_news.get_page(page_number)
        return render(request, 'index_perents.html', context={'person': student,
                                                              'menu': menu.items(),
                                                              'order_news': order_news,
                                                              'schedule': schedule.items(),
                                                              'title': f'Дневник|{student}',
                                                              'chet': [2, 4, 6],
                                                              'news': page_obj,
                                                              })


class TeacherView(View):
    def dispatch(self, request, teacher_name):
        teacher = get_object_or_404(Teacher, slug=teacher_name)
        disciplines = teacher.discipline.all()
        groups = []

        schedule = {}
        weekdays_t = Weekday.objects.all()
        weekdays_n = [0, 3, 1, 4, 2, 5]

        for n in range(0, 6):
            weekdays_n[n] = weekdays_t[weekdays_n[n]]
        for weekday in weekdays_n:
            a = ['', '', '', '', '', '']

            lessons = weekday.schedulegroup_set.filter(discipline__teacher=teacher)
            for n in range(0, 6):
                for l in lessons:
                    if l.n_group not in groups:
                        groups.append(l.n_group)
                    if l.lesson.pk == n+1:
                        a[n]=l
            schedule[weekday] = a

        choose_discipline = int(request.POST.get('discipline', '99999'))
        if choose_discipline != 99999:
            choose_discipline = Discipline.objects.get(pk=choose_discipline)
        choose_group = int(request.POST.get('group_select', '99999'))
        if choose_group != 99999:
            choose_group = StudentGroup.objects.get(pk=choose_group)
        choose_student = request.GET.get('student', 'не выбран')
        if choose_student != 'не выбран':
            choose_student = Student.objects.get(slug=choose_student)
        print(request.POST)
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

        return render(request, 'index_teach.html', context={'person': teacher,
                                                            'disciplines': disciplines,
                                                            'groups': groups,
                                                            'choose_discipline': choose_discipline,
                                                            'choose_group': choose_group,
                                                            'choose_student': choose_student,
                                                            'menu': menu.items(),
                                                            'title': f'Журнал|{teacher}',
                                                            'news': page_obj,
                                                            'schedule': schedule.items(),
                                                            'weekdays': weekdays_list.items(),
                                                            'chet': [2, 4, 6], # для отображения расписания в таблицу
                                                            #'weekday_get': weekday_get, Применяется в случае использования постраничного отображения расписанию
                                                            })





class NewsView(View):
    def get(self, request, news_slug):
        news_detail = get_object_or_404(News, slug=news_slug)
        return render(request, 'news_detail.html', context={'news': news_detail,
                                                            })


class LoginUser(LoginView):
    form_class = LoginForm
    template_name = 'login.html'

    def get_success_url(self):
        return reverse_lazy('redirect_page')


class SubmissionView(View):
    def get(self, request):
        return render(request, 'submission_form.html')


def logout_view(request):
    logout(request)
    return redirect('/login/')


def redirect_page(request):
    if request.user.groups.filter(name="Учителя"):
        return redirect(f'/teach/{request.user.username}')
    elif request.user.groups.filter(name="Студенты"):
        return redirect(f'/student/{request.user.username}')
    else:
        return redirect(f'/login/')





class HomeView(View):
    def get(self, request):\
        return redirect('/login/')