# Generated by Django 2.1.4 on 2019-01-05 01:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20190105_0223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gpspoint',
            name='record_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 1, 5, 2, 35, 26, 512834)),
        ),
        migrations.AlterField(
            model_name='route',
            name='end',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 1, 5, 2, 35, 26, 512834)),
        ),
        migrations.AlterField(
            model_name='route',
            name='start',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 1, 5, 2, 35, 26, 512834)),
        ),
    ]
