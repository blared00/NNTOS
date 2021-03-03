from django.db import models
from django.urls import reverse

#weekdays = {'пн': 'Понедельник', 'вт': 'Вторник', 'ср': 'Среда', 'чт': 'Четверг', 'пт': 'Пятница', 'сб': 'Суббота', }
weekdays = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', ]


class Student(models.Model):
    lastname = models.CharField(max_length=20, verbose_name='Фамилия')
    firstname = models.CharField(max_length=20, verbose_name='Имя')
    patronymic = models.CharField(max_length=20, verbose_name='Отчество')
    slug = models.SlugField(max_length=64, unique=True, verbose_name='URL студента')
    n_group = models.ForeignKey('StudentGroup', on_delete=models.CASCADE, verbose_name='Номер группы')

    def __str__(self):
        name = f'{self.lastname} {self.firstname} {self.patronymic}'
        return name

    def get_absolute_url(self):
        return reverse('student', kwargs={'student_name': self.slug})

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'


class StudentGroup(models.Model):
    number = models.CharField(max_length=20, verbose_name='Номер группы')

    def __str__(self):
        return self.number

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'


class Discipline(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название дисциплины')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Дисциплина'
        verbose_name_plural = 'Дисциплины'




class Teacher(models.Model):
    lastname = models.CharField(max_length=20, verbose_name='Фамилия')
    firstname = models.CharField(max_length=20, verbose_name='Имя')
    patronymic = models.CharField(max_length=20, verbose_name='Отчество')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='URL преподавателя')
    discipline = models.ManyToManyField(Discipline, verbose_name='Дисциплина')

    def __str__(self):
        name = f'{self.lastname} {self.firstname} {self.patronymic}'
        return name

    def get_absolute_url(self):
        return reverse('teacher', kwargs={'teacher_name': self.slug})

    class Meta:
        verbose_name = 'Учитель'
        verbose_name_plural = 'Учителя'



class ScheduleGroup(models.Model):
    discipline = models.ForeignKey('Discipline', on_delete=models.CASCADE, verbose_name='Дисциплина')
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE, verbose_name='Учитель')
    lesson = models.ForeignKey('NumberLesson', on_delete=models.CASCADE, verbose_name='Пара')
    class_room = models.IntegerField(verbose_name='Номер аудитории')
    weekday = models.ForeignKey('Weekday', on_delete=models.CASCADE, verbose_name='День недели')
    n_group = models.ForeignKey('StudentGroup', on_delete=models.CASCADE, verbose_name='Номер группы')

    def __str__(self):
        name = f' {self.discipline} {self.teacher}'
        return name

    class Meta:
        verbose_name = 'Пара'
        verbose_name_plural = 'Пары'



class NumberLesson(models.Model):
    time_start = models.TimeField(verbose_name='Начало пары')
    time_end = models.TimeField(verbose_name='Окончание пары')

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = 'Номер пары'
        verbose_name_plural = 'Номера пар'


class Weekday(models.Model):
    name = models.CharField(max_length=12, verbose_name='День недели')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'День недели'
        verbose_name_plural = 'Дни недели'


class News(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='URL объявления')
    description = models.TextField(verbose_name='Содержание')
    published_at = models.DateTimeField(auto_now_add=True, )
    picture = models.ImageField(upload_to='picture_newstudent/%Y/%m/%d', verbose_name='Иллюстрация', blank=True)
    published_for_parents = models.BooleanField(verbose_name='Для родителей')
    published_for_teacher = models.BooleanField(verbose_name='Для учителей')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news', kwargs={'news_slug': self.slug})

    class Meta:
        verbose_name = 'Объявление '
        verbose_name_plural = 'Объявления'
        ordering = ('-published_at', )


