from django.urls import path

from . import views
from django.views.generic.base import TemplateView

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('route/', views.route, name='route'),
    path('remove/<slug:deviceId>', views.removeTracker, name='remove'),
    path('showEdit/<slug:deviceId>', views.showOrEditTracker, name='showEdit'),
    path('add/', views.add, name='add'),
    path('statistic/', views.statistic, name='statistic'),
    path('position/', views.position, name='position'),
    path('reset/', views.change_password, name='reset'),
    path('user/', views.usr, name='usr'),
    path('open/<slug:deviceid>', views.open),
    path('close/<slug:deviceid>', views.close),
    path('record/<slug:deviceid>', views.record),
    path('deleteRoute/<int:routeid>', views.deleteRoute)
]

