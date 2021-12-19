# Generated by Django 2.1.3 on 2019-01-09 12:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20190109_1339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gpspoint',
            name='record_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 1, 9, 13, 49, 5, 685641)),
        ),
        migrations.AlterField(
            model_name='route',
            name='end',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 1, 9, 13, 49, 5, 684643)),
        ),
        migrations.AlterField(
            model_name='route',
            name='start',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 1, 9, 13, 49, 5, 684643)),
        ),
        migrations.AlterField(
            model_name='tracker',
            name='status',
            field=models.CharField(choices=[('Ab', 'Abgeschlossen'), ('Ge', 'Geoeffnet'), ('Ra', 'Route aufzeichnen'), ('Off', 'Offline')], max_length=3),
        ),
    ]
