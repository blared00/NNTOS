from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import *
# Create your views here.


class ParentsView(View):
    def get(self, request, student_name):
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
        order_news = request.GET.get('sorting')
        print(order_news)
        if order_news == 'last':
            news = News.objects.filter(published_for_parents=True).order_by('published_at')
        else:
            news = News.objects.filter(published_for_parents=True)
        paginator_news = Paginator(news, 5)
        page_number = request.GET.get('page')
        page_obj = paginator_news.get_page(page_number)
        return render(request, 'index_perents.html', context={'student': student,
                                                              'schedule': schedule.items(),
                                                              'title': f'Дневник|{student}',
                                                              'chet': [2, 4, 6],
                                                              'news': page_obj,

                                                              })


class TeacherView(View):
    def get(self, request):
        return render(request, 'index_teach.html')


class LoginView(View):
    def get(self, request):
        return render(request, 'login_form.html')


class NewsView(View):
    def get(self, request, news_slug):
        news_information = get_object_or_404(News, slug=news_slug)
        return HttpResponse(f'Здесь объявление {news_information}')
