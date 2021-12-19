# Generated by Django 2.1.3 on 2019-01-09 12:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20190105_0235'),
    ]

    operations = [
        migrations.AddField(
            model_name='tracker',
            name='device_lat',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='tracker',
            name='device_long',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='gpspoint',
            name='record_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 1, 9, 13, 39, 19, 120394)),
        ),
        migrations.AlterField(
            model_name='route',
            name='end',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 1, 9, 13, 39, 19, 119397)),
        ),
        migrations.AlterField(
            model_name='route',
            name='start',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 1, 9, 13, 39, 19, 119397)),
        ),
        migrations.AlterField(
            model_name='tracker',
            name='device_eui',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='tracker',
            name='device_name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]