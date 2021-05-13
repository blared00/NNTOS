import datetime
import time

from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import redirect

from .models import Teacher, Weekday, Mark, ScheduleGroup, weekdays, Comment


class DataMixin:
    def user_valid_page(self, person, request):
        if request.user.username != person and request.user.username != 'admin':
            return redirect('/redirectpage')
    def get_list_groups(self, person):
        groups = []
        for lesson in ScheduleGroup.objects.filter(discipline__teacher=person):
            if lesson.n_group not in groups:
                groups.append(lesson.n_group)
        return groups
    def schedule_for_person(self, person, date=f'{datetime.datetime.isocalendar(datetime.datetime.now())[0]}-W{datetime.datetime.isocalendar(datetime.datetime.now())[1]}'):
        print(date)

        schedule = {}
        weekdays_t = weekdays

        weekdays_n = [0, 3, 1, 4, 2, 5]

        dates_n = [n for n in range(6)]
        YEAR = date[:4]
        WEEK = int(date[-2:])-1  # as it starts with 0 and you want week to start from sunday
        startdate = time.asctime(time.strptime(f'{YEAR} {WEEK} 0', '%Y %W %w'))
        startdate = datetime.datetime.strptime(startdate, '%a %b %d %H:%M:%S %Y')
        dates = [startdate.strftime('%Y-%m-%d')]
        for i in range(1, 7):
            day = startdate + datetime.timedelta(days=i)
            dates.append(day.strftime('%Y-%m-%d'))


        try:
            schedule_date = ScheduleGroup.objects.filter(Q(n_group=person.n_group.pk),
                                                     Q(date__gte=dates[0]), Q(date__lte=dates[-1]))
        except AttributeError:
            schedule_date = ScheduleGroup.objects.filter(Q(discipline__teacher=person),
                                                         Q(date__gte=dates[0]), Q(date__lte=dates[-1]))
        print(f'Все пары за неделю{schedule_date}')
        for i in range(1, 7):
            day = startdate + datetime.timedelta(days=i)
            dates.append(day.strftime('%Y-%m-%d'))

        for n in range(0, 6):
            dates_n[n] = dates[weekdays_n[n]+1]
            weekdays_n[n] = weekdays_t[weekdays_n[n]]

        try:
            marks = Mark.objects.filter(Q(student=person), Q(schedule_lesson__date__gte=dates[0]), Q(schedule_lesson__date__lte=dates[-1]))

        except ValueError:
            pass

        # for weekday in weekdays_n:
        for date_for_schedule in dates_n:

            a = ['' for i in range(6)]
            # date_for_weekday = dates_n[weekdays_n.index(weekday)]
            weekday = weekdays_n[dates_n.index(date_for_schedule)]
            lessons = schedule_date.filter(date=date_for_schedule)

            # except AttributeError:
            #     lessons = weekday.schedulegroup_set.filter(discipline__teacher=person)
            for n in range(0, 6):
                for l in lessons:
                    if l.lesson.pk == n + 1:
                        try:
                            valid = person.n_group
                            mark = marks.filter(Q(schedule_lesson__discipline__pk=l.discipline.pk), Q(schedule_lesson__date=date_for_schedule)).first()
                            if not mark:
                                mark = ''
                            try:
                                mark = mark.value
                                if mark == None:
                                    mark = ''
                                elif mark == 1:
                                    mark = 'Н'
                            except:
                                pass
                            notify = Comment.objects.filter(Q(student=person), Q(schedule_lesson=l.pk)).first()
                            a[n] = {'discipline_schedule': l, 'date_schedule': date_for_schedule, 'mark': mark, 'notify': notify}
                        except AttributeError:
                            a[n] = l
            schedule[f'{weekday}, {datetime.datetime.strptime(date_for_schedule,"%Y-%m-%d").strftime("%d.%m.%Y")}'] = a

        return schedule

    def news_views(self, request, news):
        order_news = request.POST.get('sorting_news', 'first')
        if order_news == 'last':
            news = news.order_by('published_at')
        paginator_news = Paginator(news, 5)
        page_number = request.GET.get('page')
        page_obj_news = paginator_news.get_page(page_number)
        return {'page_obj_news': page_obj_news, 'order_news': order_news}
