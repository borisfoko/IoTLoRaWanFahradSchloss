from django.contrib import admin
from .models import Tracker
from .models import Route
from .models import GPSPoint

# Register your models here.

admin.site.register(Tracker)
admin.site.register(Route)
admin.site.register(GPSPoint)