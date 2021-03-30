# Generated by Django 3.1.5 on 2021-03-29 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0011_auto_20210328_1125'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ('-date',), 'verbose_name': 'комментарий', 'verbose_name_plural': 'Комментарии'},
        ),
        migrations.AlterModelOptions(
            name='mark',
            options={'ordering': ('-date',), 'verbose_name': 'Оценка ', 'verbose_name_plural': 'Оценки'},
        ),
        migrations.AlterField(
            model_name='comment',
            name='comment',
            field=models.TextField(max_length=300, verbose_name='Комментарий'),
        ),
        migrations.AlterField(
            model_name='mark',
            name='value',
            field=models.FloatField(blank=True, verbose_name='Оценка'),
        ),
    ]