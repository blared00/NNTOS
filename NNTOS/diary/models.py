from django.db import models
from django.urls import reverse

weekdays_list = {'ПН': 'Понедельник', 'ВТ': 'Вторник', 'СР': 'Среда', 'ЧТ': 'Четверг', 'ПТ': 'Пятница', 'СБ': 'Суббота', }
weekdays = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', ]


class Student(models.Model):
    """Модель студента"""
    lastname = models.CharField(max_length=20, verbose_name='Фамилия')
    firstname = models.CharField(max_length=20, verbose_name='Имя')
    patronymic = models.CharField(max_length=20, verbose_name='Отчество')
    slug = models.SlugField(max_length=64, unique=True, verbose_name='URL студента')
    n_group = models.ForeignKey('StudentGroup', on_delete=models.CASCADE, verbose_name='Номер группы')

    def __str__(self):
        """Отображение объектов с именем"""
        name = f'{self.lastname} {self.firstname} {self.patronymic}'
        return name

    def get_absolute_url(self):
        """Ссылка на страницу студента"""
        return reverse('student', kwargs={'student_name': self.slug})

    def get_abrivioture(self):
        """Абривиотура студента"""
        return f'{self.lastname} {self.firstname[0]}.{self.patronymic[0]}.'

    class Meta:
        verbose_name = 'студента'
        verbose_name_plural = 'Студенты'


class StudentGroup(models.Model):
    """Модель группы"""
    number = models.CharField(max_length=20, verbose_name='Номер группы')

    def __str__(self):
        """Отображение объектов с именем"""
        return self.number

    class Meta:
        verbose_name = 'группу'
        verbose_name_plural = 'Группы'


class Discipline(models.Model):
    """Модель дисциплины"""
    name = models.CharField(max_length=50, verbose_name='Название дисциплины')

    def __str__(self):
        """Отображение объектов с именем"""
        return self.name

    class Meta:
        verbose_name = 'дисциплину'
        verbose_name_plural = 'Дисциплины'


class Teacher(models.Model):
    """Модель преподавателя"""
    lastname = models.CharField(max_length=20, verbose_name='Фамилия')
    firstname = models.CharField(max_length=20, verbose_name='Имя')
    patronymic = models.CharField(max_length=20, verbose_name='Отчество')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='URL преподавателя')
    discipline = models.ManyToManyField(Discipline, verbose_name='Дисциплина',
                                        through='TeacherDiscipline',)

    def __str__(self):
        """Отображение объектов с именем"""
        name = f'{self.lastname} {self.firstname} {self.patronymic}'
        return name

    def get_absolute_url(self):
        """Ссылка на журнал преподавателя"""
        return reverse('teacher', kwargs={'teacher_name': self.slug})

    def get_abrivioture(self):
        """Абривиотура преподавателя"""
        return f'{self.lastname} {self.firstname[0]}.{self.patronymic[0]}.'

    class Meta:
        verbose_name = 'преподавателя'
        verbose_name_plural = 'Преподаватели'


class TeacherDiscipline(models.Model):
    """Модель взаимосвязи преподавателя и дисциплины"""
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE, verbose_name='Преподаватель')
    discipline = models.ForeignKey('Discipline', on_delete=models.CASCADE, verbose_name='Дисциплина')
    name = models.CharField(max_length=200, verbose_name="Дисциплина/Преподаватель", )

    def __str__(self):
        """Отображение объектов с именем"""
        name = f'{self.discipline}/{self.teacher.get_abrivioture()}'
        return name

    class Meta:
        verbose_name = 'предмет'
        verbose_name_plural = 'Дисциплины учителя'
        unique_together = ('discipline', 'teacher')


class ScheduleGroup(models.Model):
    discipline = models.ForeignKey('TeacherDiscipline', on_delete=models.CASCADE, verbose_name='Дисциплина')
    lesson = models.ForeignKey('NumberLesson', on_delete=models.CASCADE, verbose_name='Номер пары')
    class_room = models.IntegerField(verbose_name='Номер аудитории')
    n_group = models.ForeignKey('StudentGroup', on_delete=models.CASCADE, verbose_name='Номер группы')
    date = models.DateField(verbose_name="Дата")

    def __str__(self):
        return f'{self.date}/{self.discipline} '

    class Meta:
        verbose_name = 'элемент расписания'
        verbose_name_plural = 'Пары'
        unique_together = (('date', 'lesson', 'discipline'), )


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
    picture1 = models.ImageField(upload_to='picture_news/%Y/%m/%d-1', verbose_name='Иллюстрация 1', blank=True)
    picture2 = models.ImageField(upload_to='picture_news/%Y/%m/%d-2', verbose_name='Иллюстрация 2', blank=True)
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


class Mark(models.Model):
    value = models.IntegerField(verbose_name='Оценка', blank=True, null=True)
    student = models.ForeignKey('Student', on_delete=models.CASCADE, verbose_name='Студент')
    schedule_lesson = models.ForeignKey('ScheduleGroup', on_delete=models.CASCADE, verbose_name='Пара')
    mean_b = models.BooleanField()

    def __str__(self):
        return f'{self.schedule_lesson} {self.student}'

    class Meta:
        verbose_name = 'Оценка '
        verbose_name_plural = 'Оценки'
        ordering = ('-schedule_lesson',)
        unique_together = ('student', 'schedule_lesson')


class Comment(models.Model):
    comment = models.TextField(max_length=300, verbose_name='Комментарий')
    student = models.ForeignKey('Student', on_delete=models.CASCADE, verbose_name='Студент')
    schedule_lesson = models.ForeignKey('ScheduleGroup', on_delete=models.CASCADE, verbose_name='Пара')

    def __str__(self):
        return f'{self.schedule_lesson} {self.student}'

    def get_absolute_url(self):
        return reverse('comment', kwargs={'comment': self.pk})

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-schedule_lesson',)
