# Generated by Django 2.1.3 on 2019-01-18 11:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_auto_20190116_1422'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gpspoint',
            name='record_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 1, 18, 12, 49, 27, 122698)),
        ),
        migrations.AlterField(
            model_name='route',
            name='start',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 1, 18, 12, 49, 27, 121819)),
        ),
    ]
