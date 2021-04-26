import datetime
import time

from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import redirect

from .models import Teacher, Weekday, Mark, ScheduleGroup, weekdays


class DataMixin:
    def user_valid_page(self, person, request):
        if request.user.username != person and request.user.username != 'admin':
            return redirect('/redirectpage')
    def schedule_for_person(self, person, date=f'{datetime.datetime.isocalendar(datetime.datetime.now())[0]}-W{datetime.datetime.isocalendar(datetime.datetime.now())[1]}'):
        groups = []
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

        for i in range(1, 7):
            day = startdate + datetime.timedelta(days=i)
            dates.append(day.strftime('%Y-%m-%d'))

        for n in range(0, 6):
            dates_n[n] = dates[weekdays_n[n]+1]
            weekdays_n[n] = weekdays_t[weekdays_n[n]]

        try:
            marks = Mark.objects.filter(Q(student=person), Q(date__gte=dates[0]), Q(date__lte=dates[-1]))

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
                    if l.n_group not in groups:
                        groups.append(l.n_group)
                    if l.lesson.pk == n + 1:
                        try:
                            valid = person.n_group
                            a[n] = {'discipline_schedule': l, 'date_schedule': date_for_schedule, 'mark': marks.filter(Q(discipline__pk=l.discipline.pk), Q(date=date_for_schedule)).first}
                        except AttributeError:
                            a[n] = l
            schedule[f'{weekday}, {datetime.datetime.strptime(date_for_schedule,"%Y-%m-%d").strftime("%d.%m.%Y")}'] = a

        return {'groups': groups, 'schedule': schedule}

    def news_views(self, request, news):
        order_news = request.POST.get('sorting_news', 'first')
        if order_news == 'last':
            news = news.order_by('published_at')
        paginator_news = Paginator(news, 5)
        page_number = request.GET.get('page')
        page_obj_news = paginator_news.get_page(page_number)
        return {'page_obj_news': page_obj_news, 'order_news': order_news}
