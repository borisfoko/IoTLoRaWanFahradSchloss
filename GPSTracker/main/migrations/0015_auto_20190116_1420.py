# Generated by Django 2.1.3 on 2019-01-16 13:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_auto_20190115_1227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gpspoint',
            name='record_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 1, 16, 14, 20, 29, 525273)),
        ),
        migrations.AlterField(
            model_name='route',
            name='start',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 1, 16, 14, 20, 29, 524276)),
        ),
    ]
