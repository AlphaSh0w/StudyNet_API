# Generated by Django 3.2 on 2021-04-18 13:55

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Sessions', '0005_alter_sessionhistory_action_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sessionhistory',
            name='action_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='action date'),
        ),
    ]
