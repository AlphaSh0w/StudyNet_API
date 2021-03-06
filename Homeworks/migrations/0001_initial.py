# Generated by Django 3.2 on 2021-05-08 17:32

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Management', '0001_initial'),
        ('Accounts', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='HomeworkHistory',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False, verbose_name='id')),
                ('module_type', models.CharField(choices=[('LECTURE', 'Lecture'), ('DIRECTED', 'Directed studies'), ('PRACTICAL', 'Practical work')], max_length=15, verbose_name='module type')),
                ('concerned_groups', django.contrib.postgres.fields.ArrayField(base_field=models.PositiveSmallIntegerField(), size=None, verbose_name='concerned groups')),
                ('title', models.CharField(max_length=150, verbose_name='title')),
                ('due_date', models.DateTimeField(verbose_name='due date')),
                ('comment', models.TextField(blank=True, verbose_name='comment')),
                ('action_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='action date')),
                ('action_type', models.CharField(choices=[('ADD', 'Add'), ('UPDATE', 'Update'), ('DELETE', 'Delete')], max_length=15, verbose_name='action type')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='author')),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='Management.module', verbose_name='module')),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='Management.section', verbose_name='section')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='Accounts.teacher', verbose_name='teacher')),
            ],
            options={
                'verbose_name': 'Homework history',
                'verbose_name_plural': 'Homeworks history',
            },
        ),
        migrations.CreateModel(
            name='Homework',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False, verbose_name='id')),
                ('concerned_groups', django.contrib.postgres.fields.ArrayField(base_field=models.PositiveSmallIntegerField(), size=None, verbose_name='concerned groups')),
                ('title', models.CharField(max_length=150, verbose_name='title')),
                ('due_date', models.DateTimeField(verbose_name='due date')),
                ('comment', models.TextField(blank=True, verbose_name='comment')),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Management.assignment', verbose_name='assignment')),
            ],
            options={
                'verbose_name': 'Homework',
                'verbose_name_plural': 'Homeworks',
            },
        ),
    ]
