# Generated by Django 3.2 on 2021-04-16 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Management', '0004_auto_20210416_1821'),
        ('Accounts', '0005_auto_20210416_1821'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='sections',
            field=models.ManyToManyField(through='Management.TeacherSection', to='Management.Section', verbose_name='sections'),
        ),
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False, verbose_name='id'),
        ),
        migrations.DeleteModel(
            name='TeacherSection',
        ),
    ]
