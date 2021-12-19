import datetime

from django.db import models
from django.conf import settings

	
class Tracker(models.Model):
	STATUS_CHOISES = (
        ('Ab', 'Abgeschlossen'),
        ('Ge', 'Geöffnet'),
		('Ra', 'Route aufzeichnen')
    )
	CONNECT_CHOISES = (
		('Off', 'Verbindung unterbrochen'),
		('On', 'Verbindung aktiv'),
		('GPS', 'GPS Funkloch')
	)
	device_name = models.CharField(max_length=50)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	status = models.CharField(max_length=3, choices=STATUS_CHOISES)
	connect_status = models.CharField(max_length=3, choices=CONNECT_CHOISES)
	device_eui = models.CharField(unique=True, max_length=50)

	def addTracker(self):
		self.save()
	
	def __str__(self):
		return self.device_eui
	
class Route(models.Model):
	start = models.DateTimeField(default=datetime.datetime.now(), blank=True)
	end = models.DateTimeField(null=True)
	tracker = models.ForeignKey(Tracker, on_delete=models.CASCADE, null=True)

class GPSPoint(models.Model):
	tracker = models.ForeignKey(Tracker, on_delete=models.CASCADE, null=True)
	record_date = models.DateTimeField( blank=True, null=True)
	device_long = models.CharField(max_length=30, null=True)
	device_lat = models.CharField(max_length=30, null=True)
	device_alt = models.CharField(max_length=30, null=True)