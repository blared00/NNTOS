"""NNTOS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include
from diary.views import  ParentsView, TeacherView,CommentView, NewsView, LoginUser, HomeView, logout_view, redirect_page, MarkView
from NNTOS.settings import MEDIA_URL, MEDIA_ROOT



urlpatterns = [
    path('admin/', admin.site.urls),
    path('student/<slug:student_name>', ParentsView.as_view(), name='student'),
    path('teach/<slug:teacher_name>', TeacherView.as_view(), name='teacher'),
    path('news/<slug:news_slug>', NewsView.as_view(), name='news'),
    path('comment/<int:comment>', CommentView.as_view(), name='comment'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('redirectpage/', redirect_page, name='redirect_page'),
    path('formmark/', MarkView.as_view(), name='markview'),
    # path('formmark/edit/', MarkEditView.as_view(), name='markeditview'),
    path('grappelli/', include('grappelli.urls')), # grappelli URLS
    path('', HomeView.as_view(), name='home')

]
urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
