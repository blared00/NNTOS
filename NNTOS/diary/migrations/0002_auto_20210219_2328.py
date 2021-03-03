# Generated by Django 3.1.5 on 2021-02-19 20:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedulegroup',
            name='n_group',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='diary.studentgroup', verbose_name='Номер группы'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='schedulegroup',
            name='weekday',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='diary.weekday', verbose_name='День недели'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='schedulegroup',
            name='lesson',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='diary.numberlesson', verbose_name='Пара'),
        ),

    ]
