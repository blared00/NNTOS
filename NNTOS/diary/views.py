import datetime

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.views import LoginView
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db.models import Q
from django.forms import formset_factory
from django.template import RequestContext

from .form import CommentForm, MarkForm
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from .form import LoginForm
from .models import *
# Create your views here.
from .utils import DataMixin




class ParentsView(DataMixin, View):

    def dispatch(self, request, student_name):
        ''' Получение предметов студента и отображение расписания'''
        student = get_object_or_404(Student, slug=student_name)
        user = request.user
        if not request.user.is_authenticated:
            return redirect('/login/')
        if self.user_valid_page(student_name, request):          #Проверка входа на личную страницу
            return self.user_valid_page(student_name, request)
        date_now = datetime.datetime.isocalendar(datetime.datetime.now())
        date_selected = request.POST.get('sorting_week', f'{date_now[0]}-W{date_now[1]}')

        schedule = self.schedule_for_person(student, date=date_selected) #Получение предметов студента и отображение расписания

        menu = {'#glavnaya': 'Главная',                          #Разделы навбара
                '#dosca': 'Доска объявлений',
                '#dnevnik': 'Электронный дневник',
                '#uved': 'Уведомления'
                }

        news = News.objects.filter(published_for_parents=True)
        news = self.news_views(request, news)



        submission = Comment.objects.filter(student=student)
        order_sub = request.POST.get('sorting_notify', 'first')
        if order_sub == 'last':
            submission = submission.order_by('date')
        paginator_news = Paginator(submission, 5)
        page_number_sub = request.GET.get('page_sub')
        page_obj_sub = paginator_news.get_page(page_number_sub)
        return render(request, 'index_perents.html', context={'person': student,
                                                              'user': user,
                                                              'menu': menu.items(),
                                                              'order_news': news['order_news'],
                                                              'order_sub': order_sub,
                                                              'schedule': schedule.items(),
                                                              'title': f'Дневник|{student}',
                                                              'chet': [2, 4, 6],
                                                              'news': news['page_obj_news'],
                                                              'submission': page_obj_sub,
                                                              'week_selected': date_selected,
                                                              })


class TeacherView(DataMixin, View):
    def dispatch(self, request, teacher_name):
        teacher = get_object_or_404(Teacher, slug=teacher_name)
        user = request.user
        if not request.user.is_authenticated:
            return redirect('/login/')
        self.change_email_user(request)

        if self.user_valid_page(teacher_name, request):
            return self.user_valid_page(teacher_name, request)
        disciplines = teacher.discipline.all()
        groups = self.get_list_groups(teacher)
        date_now = datetime.datetime.isocalendar(datetime.datetime.now())
        date_selected = request.POST.get('sorting_week', f'{date_now[0]}-W{date_now[1]}')

        schedule = self.schedule_for_person(teacher, date=date_selected)

        '''Переменные для работы формы "Комментарий ученику" '''

        if request.method == 'GET':     # Задаем переменные для первого запуска страницы
            choose_discipline = request.GET.get('discipline_get', 99999)
            choose_group = request.GET.get('group_get', 99999)

        else: # метод пост вызывается в том случае, если происходит выбор группы или дисциплины
            choose_discipline = request.POST.get('discipline_select', 99999) # Получение значения из select
            choose_group = request.POST.get('group_select', 99999)
        choose_student = request.GET.get('student_select', 'не выбран')
        choose_teacherdiscipline = ''
        try:
            choose_discipline = Discipline.objects.get(pk=choose_discipline)
            choose_group = StudentGroup.objects.get(pk=choose_group)
            choose_student = Student.objects.get(slug=choose_student)

        except Discipline.DoesNotExist:
            pass
        except Student.DoesNotExist:
            pass
        except StudentGroup.DoesNotExist:
            pass
        try:
            choose_teacherdiscipline = TeacherDiscipline.objects.get(Q(teacher=teacher), Q(discipline=choose_discipline))
        except TeacherDiscipline.DoesNotExist:
            pass
        list_date = ScheduleGroup.objects.filter(Q(discipline__teacher=teacher), Q(discipline__discipline=choose_discipline), Q(n_group=choose_group))
        list_dat =[n for n in list_date.order_by('date')]
        list_dat.append(' ')
        paginator_list_date = Paginator(list_dat, 9)
        page_number = request.GET.get('page_marks')
        page_obj_list_date = paginator_list_date.get_page(page_number)

        marks_student = {}
        paginator_marks = {}
        page_obj_marks = {'':''}
        last_student = ''
        try:

            for student in choose_group.student_set.all():
                marks_student[student] = []
                for marks in list_date.filter(n_group=choose_group).order_by('date'):
                    try:
                        if marks.mark_set.all().filter(student=student).first().value == 1:
                            marks_student[student].append({'value': 'Н',
                                                      'mean_b': marks.mark_set.all().filter(student=student).first().mean_b})
                        else:
                            marks_student[student].append(marks.mark_set.all().filter(student=student).first())
                    except AttributeError:
                        marks_student[student].append( {'value': '',
                                                  'mean_b': False})
                # marks_student[student] = [{'value': 'Н', 'mean_b':marks.mark_set.all().filter(student=student).first().mean_b }
                #                           if marks.mark_set.all().filter(student=student).first().value == 1
                #                           else marks.mark_set.all().filter(student=student).first()
                #                           for marks in list_date.filter(n_group=choose_group).order_by('date')]
                average_mark = 0
                num_mark = 0
                for mark in marks_student[student]:
                    try:
                        if mark.value and mark.mean_b:
                            average_mark += mark.value
                            num_mark += 1
                    except AttributeError:
                        pass
                if num_mark:
                    average_mark /= num_mark

                marks_student[student].append({'value':round(average_mark,1), 'avg': True})

            for student, marks in marks_student.items():
                paginator_marks[student] = Paginator(marks, 9)
                page_number = request.GET.get('page_marks')
                page_obj_marks[student] = paginator_marks[student].get_page(page_number)
                last_student = student
        except AttributeError as e:
            print(e)
        # if choose_discipline != 99999 and choose_group != 99999:
        page_obj_marks.pop('')
        form_submission = CommentForm()
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
        news = self.news_views(request, news)



        return render(request, 'index_teach.html', context={'person': teacher,
                                                            'disciplines': disciplines,
                                                            'groups': groups,
                                                            'user': user,
                                                            'choose_discipline': choose_discipline,
                                                            'choose_teacherdiscipline': choose_teacherdiscipline,
                                                            'choose_group': choose_group,
                                                            'choose_student': choose_student,
                                                            'form_submission': form_submission,
                                                            'menu': menu.items(),
                                                            'title': f'Журнал|{teacher}',
                                                            'news': news['page_obj_news'],
                                                            'order_news': news['order_news'],
                                                            'schedule': schedule.items(),
                                                            'weekdays': weekdays_list.items(),
                                                            'chet': [2, 4, 6], # для отображения расписания в таблицу
                                                            'week_selected': date_selected,
                                                            'list_date': page_obj_list_date,
                                                            'marks_student': page_obj_marks.items(),
                                                            'marks_paginator': page_obj_marks[last_student] if last_student in page_obj_marks else ''

                                                            #'weekday_get': weekday_get, Применяется в случае использования постраничного отображения расписанию
                                                            })





class NewsView(View):
    def dispatch(self, request, news_slug):
        if not request.user.is_authenticated:
            return redirect('/login/')
        news_detail = get_object_or_404(News, slug=news_slug)
        return render(request, 'news_detail.html', context={'news': news_detail,
                                                            })

class CommentView(View):
    def dispatch(self, request, comment):
        if not request.user.is_authenticated:
            return redirect('/login/')
        comment_detail = get_object_or_404(Comment, pk=comment)
        return render(request, 'read_notify.html', context={'comment': comment_detail,
                                                            })

class LoginUser(LoginView):
    form_class = LoginForm
    template_name = 'login.html'
    redirect_authenticated_user = True


    def get_success_url(self):
        return reverse_lazy('redirect_page')


def logout_view(request):
    logout(request)
    return redirect('/login/')


def redirect_page(request):
    if request.user.is_superuser:
        return redirect(f'/admin/')
    if request.user.groups.filter(name="Учителя"):
        return redirect(f'/teach/{request.user.username}'if request.user.email else f'/teach/{request.user.username}#email_form')
    elif request.user.groups.filter(name="Студенты"):
        return redirect(f'/student/{request.user.username}'if request.user.email else f'/student/{request.user.username}#email_form')
    else:
        return redirect(f'/login/')



class HomeView(View):
    def get(self, request):\
        return redirect('/login/')


class MarkView(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/login/')

        if request.POST.get('discipline', '') and request.POST['group_select']:
            choose_group = request.POST.get('group_select', 'не выбрана')
            choose_discipline = request.POST.get('discipline', 'не выбран')
        else:
            print("тут считаю")
            choose_discipline = request.GET.get('dis', 'не выбран')
            choose_group = request.GET.get('group', 'не выбрана')
        extra_form = 0
        if choose_discipline != 'не выбран':
            try:
                choose_discipline = TeacherDiscipline.objects.get(pk=choose_discipline)
            except TeacherDiscipline.DoesNotExist:
                choose_discipline = 'не выбран'

        if choose_group != 'не выбрана':
            try:
                choose_group = StudentGroup.objects.get(pk=choose_group)
                extra_form = len(choose_group.student_set.all())
            except StudentGroup.DoesNotExist:
                choose_group = 'не выбрана'

        schedule = ScheduleGroup.objects.filter(Q(n_group=choose_group),Q(discipline=choose_discipline))
        MarkFormFormSet = formset_factory(MarkForm, extra=extra_form)
        formset = MarkFormFormSet()

        rangee = len(choose_group.student_set.all())
        students = [choose_group.student_set.all()[n] for n in range(rangee)]
        sdasd = {students[n]: '' for n in range(rangee)}

        data_mark = request.POST.get('datamark', 'не выбрана')
        try:
            data_mark = ScheduleGroup.objects.get(pk=data_mark)
        except:
            pass
        flag = request.POST.get('flags', False)
        if data_mark != 'не выбрана':
            try:
                formset = MarkFormFormSet(request.POST or None)
                if formset.is_valid():
                    flag = 0
                    messages.success(request, "Оценки сохранены")
                    if not flag:
                        for form in formset:
                            form.save()


                    formset = MarkFormFormSet()

                    return redirect(f'/formmark/?dis={choose_discipline.pk}&group={choose_group.pk}')
                else:
                    try:
                        marks = [students[n].mark_set.filter(schedule_lesson=data_mark).first() for n in range(rangee)]
                        sdasd = {students[n]: marks[n].value for n in range(rangee)}


                        if flag == '1':
                            for n in range(rangee):
                                if request.POST[f'form-{n}-value']:
                                    try:
                                        marks[n].value = int(request.POST[f'form-{n}-value'])
                                    except ValueError:
                                        marks[n].value = 1
                                else:
                                    marks[n].value = None
                                if request.POST[f'form-{n}-mean_b'] == 'true':
                                    marks[n].mean_b = True
                                else:
                                    marks[n].mean_b = False
                                marks[n].save()
                            messages.success(request, "Оценки сохранены")
                            flag = 0
                            return redirect(f'/formmark/?dis={choose_discipline.pk}&group={choose_group.pk}')


                        if flag=='False':
                            flag = 1
                            messages.error(request, "Оценки не сохранены.\n На эту дату есть оценки, они представлены ниже      \n — Чтобы редактировать значения, измените их и нажмите 'Сохранить'    ‌‌‍‍ \n — Чтобы отменить операцию, нажмите 'Назад'")
                        else:
                            print('ghbdtn')
                    except AttributeError as e:
                        print(e)
            except ValidationError:
               print(ValidationError)


        return render(request, 'marks_form2.html', context={'c_discipline': choose_discipline,
                                                            'c_group': choose_group,
                                                            'formset': formset,
                                                            'data_mark': data_mark,
                                                            'students': sdasd.items(),
                                                            'flag': flag,
                                                            'schedule': schedule,
                                                            })


