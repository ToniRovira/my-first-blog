# Generated by Django 2.1.3 on 2019-02-05 16:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0015_auto_20190205_1642'),
    ]

    operations = [
        migrations.AlterField(
            model_name='concesio',
            name='end_time',
            field=models.DateTimeField(default=datetime.datetime(2019, 2, 5, 17, 5, 18, 453111), verbose_name='Data final'),
        ),
        migrations.AlterField(
            model_name='concesio',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2019, 2, 5, 17, 5, 18, 453111), verbose_name='Data inici'),
        ),
    ]
