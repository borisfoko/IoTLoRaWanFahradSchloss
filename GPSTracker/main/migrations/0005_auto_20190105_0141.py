# Generated by Django 2.1.4 on 2019-01-05 00:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20190105_0133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gpspoint',
            name='record_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 1, 5, 1, 41, 29, 72916)),
        ),
        migrations.AlterField(
            model_name='route',
            name='end',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 1, 5, 1, 41, 29, 72916)),
        ),
        migrations.AlterField(
            model_name='route',
            name='start',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 1, 5, 1, 41, 29, 72916)),
        ),
    ]
