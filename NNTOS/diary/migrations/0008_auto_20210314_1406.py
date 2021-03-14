# Generated by Django 3.1.5 on 2021-03-14 11:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0007_auto_20210313_2100'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=50, verbose_name='Комментарий')),
                ('date', models.DateField()),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='diary.student')),
            ],
            options={
                'verbose_name': 'комментарий',
                'verbose_name_plural': 'Комментарии',
            },
        ),
        migrations.RemoveField(
            model_name='mark',
            name='comment',
        ),
        migrations.DeleteModel(
            name='Testik',
        ),
    ]