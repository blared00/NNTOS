from django.core.paginator import Paginator
from django.shortcuts import redirect

from .models import Teacher, Weekday


class DataMixin:
    def user_valid_page(self, person, request):
        if request.user.username != person and request.user.username != 'admin':
            return redirect('/redirectpage')
    def schedule_for_person(self, person):
        groups = []
        schedule = {}
        weekdays_t = Weekday.objects.all()
        weekdays_n = [0, 3, 1, 4, 2, 5]

        for n in range(0, 6):
            weekdays_n[n] = weekdays_t[weekdays_n[n]]
        for weekday in weekdays_n:
            a = ['', '', '', '', '', '']
            try:
                lessons = weekday.schedulegroup_set.filter(n_group=person.n_group)
            except AttributeError:
                lessons = weekday.schedulegroup_set.filter(discipline__teacher=person)
            for n in range(0, 6):
                for l in lessons:
                    if l.n_group not in groups:
                        groups.append(l.n_group)
                    if l.lesson.pk == n + 1:
                        a[n] = l
            schedule[weekday] = a
        return {'groups': groups, 'schedule': schedule}

    def news_views(self, request, news):
        order_news = request.POST.get('sorting_news', 'first')
        if order_news == 'last':
            news = news.order_by('published_at')
        paginator_news = Paginator(news, 5)
        page_number = request.GET.get('page')
        page_obj_news = paginator_news.get_page(page_number)
        return {'page_obj_news': page_obj_news, 'order_news': order_news}
