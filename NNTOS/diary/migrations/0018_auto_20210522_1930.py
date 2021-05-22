# Generated by Django 3.1.5 on 2021-05-22 16:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0017_auto_20210429_0708'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacherdiscipline',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='diary.teacher', verbose_name='Преподаватель'),
        ),
        migrations.AlterUniqueTogether(
            name='teacherdiscipline',
            unique_together={('discipline', 'teacher')},
        ),
    ]
