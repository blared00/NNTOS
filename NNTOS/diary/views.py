from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.db.models import Q

from .form import CommentForm
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
        menu = {'#glavnaya': 'Главная',
                '#dosca': 'Доска объявлений',
                '#dnevnik': 'Электронный дневник',
                '#uved': 'Уведомления'
                }
        ''' Отображение новостей и пагинация'''
        news = News.objects.filter(published_for_parents=True)
        order_news = request.POST.get('sorting_news', 'first')
        if order_news == 'last':
            news = news.order_by('published_at')
        paginator_news = Paginator(news, 5)
        page_number = request.GET.get('page')
        page_obj_news = paginator_news.get_page(page_number)
        ''' Отображение комментариев от учителей и пагинация'''
        submission = Comment.objects.filter(student=student)
        order_sub = request.POST.get('sorting_notify', 'first')
        if order_sub == 'last':
            submission = submission.order_by('date')
        paginator_news = Paginator(submission, 5)
        page_number_sub = request.GET.get('page_sub')
        page_obj_sub = paginator_news.get_page(page_number_sub)
        return render(request, 'index_perents.html', context={'person': student,
                                                              'menu': menu.items(),
                                                              'order_news': order_news,
                                                              'order_sub': order_sub,
                                                              'schedule': schedule.items(),
                                                              'title': f'Дневник|{student}',
                                                              'chet': [2, 4, 6],
                                                              'news': page_obj_news,
                                                              'submission': page_obj_sub,
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
        ''' Переменные для работы формы "Комментарий ученику" '''
        if request.method == 'GET':     # Задаем переменные для первого запуска страницы
            choose_teacherdiscipline = '' # (первый запуск происходит методом GET)
            choose_student = ''
            form_submission = CommentForm()
            if request.GET.get('discipline_get'): # если переход на страницу был осуществлен после создания комментария
                choose_discipline = request.GET.get('discipline_get')
                choose_discipline = Discipline.objects.get(pk=choose_discipline)
            else:
                choose_discipline = '0'
            if request.GET.get('group_get'): # аналогично с прим. выше
                choose_group = request.GET.get('group_get')
                choose_group = StudentGroup.objects.get(pk=choose_group)
            else:
                choose_group = '0'

        if request.method == 'POST': # метод пост вызывается в том случае, если происходит выбор группы или дисциплины
            choose_discipline = int(request.POST.get('discipline_select', '0')) # Получение значения из select
            if choose_discipline != 0:
                choose_discipline = Discipline.objects.get(pk=choose_discipline)
            choose_group = int(request.POST.get('group_select', '0'))
            if choose_group != 0:
                choose_group = StudentGroup.objects.get(pk=choose_group)
            choose_student = request.GET.get('student_select', 'не выбран')
            if choose_student != 'не выбран':
                choose_student = Student.objects.get(slug=choose_student)
            if choose_group == 0 or choose_discipline == 0:
                choose_teacherdiscipline = ''
            else:
                choose_teacherdiscipline = TeacherDiscipline.objects.get(Q(teacher=teacher), Q(discipline=choose_discipline))

            form_submission = CommentForm(request.POST) # заполнение формы к комментарию

            if form_submission.is_valid():
                if request.POST['comment'] == '':
                    form_submission = CommentForm() # Создание пустой формы для заполнения
                else:
                    form_submission.save() # если комментарий не пустой, преходит на страницу с открытым журналом и выбранными ранее "Группой" и "дисциплиной"
                    return redirect(f'/teach/{teacher.slug}?discipline_get={choose_discipline.pk}&group_get={choose_group.pk}#journal')




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
        order_news = request.POST.get('sorting_news', 'first')
        if order_news == 'last':
            news = news.order_by('published_at')
        paginator_news = Paginator(news, 5)
        page_number = request.GET.get('page')
        page_obj = paginator_news.get_page(page_number)

        return render(request, 'index_teach.html', context={'person': teacher,
                                                            'disciplines': disciplines,
                                                            'groups': groups,
                                                            'choose_discipline': choose_discipline,
                                                            'choose_teacherdiscipline': choose_teacherdiscipline,
                                                            'choose_group': choose_group,
                                                            'choose_student': choose_student,
                                                            'form_submission': form_submission,
                                                            'menu': menu.items(),
                                                            'title': f'Журнал|{teacher}',
                                                            'news': page_obj,
                                                            'order_news': order_news,
                                                            'schedule': schedule.items(),
                                                            'weekdays': weekdays_list.items(),
                                                            'chet': [2, 4, 6], # для отображения расписания в таблицу
                                                            #'weekday_get': weekday_get, Применяется в случае использования постраничного отображения расписанию
                                                            })





class NewsView(View):
    def dispatch(self, request, news_slug):
        news_detail = get_object_or_404(News, slug=news_slug)
        return render(request, 'news_detail.html', context={'news': news_detail,
                                                            })


class LoginUser(LoginView):
    form_class = LoginForm
    template_name = 'login.html'

    def get_success_url(self):
        return reverse_lazy('redirect_page')


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


'''def submission(request):
    form = CommentForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            print(request.POST.cleaned_data)
        else:
            print("vsevhuynya")

    return render(request, 'submission_form.html', context={'form_submission': form})
'''