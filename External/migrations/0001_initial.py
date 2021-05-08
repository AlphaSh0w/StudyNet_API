# Generated by Django 3.2 on 2021-05-08 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AppVersionSupport',
            fields=[
                ('version', models.CharField(max_length=30, primary_key=True, serialize=False, verbose_name='version')),
                ('is_supported', models.BooleanField(verbose_name='is supported')),
            ],
            options={
                'verbose_name': 'App version support',
                'verbose_name_plural': 'App versions support',
            },
        ),
    ]
