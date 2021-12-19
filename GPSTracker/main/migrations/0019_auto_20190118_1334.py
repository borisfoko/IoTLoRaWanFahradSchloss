# Generated by Django 2.1.3 on 2019-01-18 12:34

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_auto_20190118_1326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gpspoint',
            name='tracker',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Tracker'),
        ),
        migrations.AlterField(
            model_name='route',
            name='start',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 1, 18, 13, 34, 14, 309979)),
        ),
    ]