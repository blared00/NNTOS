from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.db.models import Q
from django.forms import formset_factory

from .form import CommentForm, MarkForm
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
            choose_discipline = request.GET.get('discipline_get', 99999)
            choose_group = request.GET.get('group_get', 99999)

        else: # метод пост вызывается в том случае, если происходит выбор группы или дисциплины
            choose_discipline = request.POST.get('discipline_select', 99999) # Получение значения из select
            choose_group = request.POST.get('group_select', 99999)
        if choose_discipline != 99999:
            choose_discipline = Discipline.objects.get(pk=choose_discipline)

        if choose_group != 99999:
            choose_group = StudentGroup.objects.get(pk=choose_group)
        choose_student = request.GET.get('student_select', 'не выбран')
        if choose_student != 'не выбран':
            choose_student = Student.objects.get(slug=choose_student)
        if choose_group == 99999 or choose_discipline == 99999:
            choose_teacherdiscipline = ''
        else:
            choose_teacherdiscipline = TeacherDiscipline.objects.get(Q(teacher=teacher), Q(discipline=choose_discipline))
        form_submission =CommentForm()
        if request.method == "POST":
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


class MarkView(View):
    def dispatch(self, request, *args, **kwargs):

        choose_discipline = request.GET.get('dis','не выбран')
        if choose_discipline != 'не выбран':
            try:
                choose_discipline = TeacherDiscipline.objects.get(pk=choose_discipline)
            except TeacherDiscipline.DoesNotExist:
                choose_discipline = 'не выбран'
        choose_group = request.GET.get('group','не выбрана')
        if choose_group != 'не выбрана':
            try:
                choose_group = StudentGroup.objects.get(pk=choose_group)
                extra_form = len(choose_group.student_set.all())
            except StudentGroup.DoesNotExist:
                extra_form = 0
                choose_group = 'не выбрана'
        else:
            extra_form = 0




        data_mark = request.POST.get('datamark', 'не выбрана')
        MarkFormFormSet = formset_factory(MarkForm, extra=extra_form)

        formset = MarkFormFormSet(request.POST or None)

        if formset.is_valid():
            messages.success(request, "Оценки сохранены")
            for form in formset:
                form.save()

            return redirect(f'/formmark/?dis={choose_discipline.pk}&group={choose_group.pk}')




        return render(request, 'marks_form2.html', context={'c_discipline': choose_discipline,
                                                            'c_group': choose_group,
                                                            'formset': formset,
                                                            'data_mark': data_mark,
                                                            })
