from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from diary.views import  ParentsView, TeacherView,CommentView, NewsView, LoginUser, HomeView, logout_view, redirect_page, MarkView
from NNTOS.settings import MEDIA_URL, MEDIA_ROOT, DEBUG
"""URL-адреса платформы"""


urlpatterns = [
    path('admin/', admin.site.urls),                                            #админ.панель
    path('student/<slug:student_name>', ParentsView.as_view(), name='student'), #страница студента
    path('teach/<slug:teacher_name>', TeacherView.as_view(), name='teacher'),   #страница преподавателя
    path('news/<slug:news_slug>', NewsView.as_view(), name='news'),             #детали новости
    path('comment/<int:comment>', CommentView.as_view(), name='comment'),       #детали комментария
    path('login/', LoginUser.as_view(), name='login'),                          #страница входа
    path('logout/', logout_view, name='logout'),                                #страница для работы системы выхода
    path('redirectpage/', redirect_page, name='redirect_page'),                 #страница для работы системы перенаправления по авторизованному пользователю
    path('formmark/', MarkView.as_view(), name='markview'),                     #страница проставления оценок
    path('grappelli/', include('grappelli.urls')), # grappelli URLS             #админ.панель доп функции
    path('', HomeView.as_view(), name='home'),                                  

    # Восстановление пароля
    path('change-password/', auth_views.PasswordResetView.as_view(template_name='step1.html'), name='reset_password'),
    path('change-password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='step2.html'), name='password_reset_done'),
    path('change/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='step3.html'), name='password_reset_confirm'),
    path('change-password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='step4.html'), name='password_reset_complete'),

]
"""Отображение статических файлов(изображений и т.п.) при открытии на локальном сервере"""
if DEBUG:
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
