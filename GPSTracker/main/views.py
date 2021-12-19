from django.shortcuts import render
from django.http import HttpResponse
from .forms import AddForm
from .forms import UserForm
from django.http import HttpResponseRedirect
from .forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from .models import Tracker, GPSPoint, Route
from django.contrib.auth.models import User
from operator import itemgetter
from datetime import datetime, timedelta


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

def change_password(request):
    if (request.user.is_authenticated):
        if request.method == 'POST':
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)  # Important!
                messages.success(request, 'Your password was successfully updated!')
                return redirect('position')
            else:
                messages.error(request, 'Please correct the error below.')
        else:
            form = PasswordChangeForm(request.user)
        return render(request, 'registration/reset.html', {
            'form': form
        })
    else:
        return render(request, 'registration/reset.html', {
            'form': None
        })

#add tracker
def add(request):
    if (request.user.is_authenticated):
        if request.method == 'POST':
            form = AddForm(request.POST)
            if form.is_valid():
                tracker = form.save(commit=False)
                #app_id = "lorawanvsschloss_11382"
                #access_key = "ttn-account-v2.8YZ1L3PZAG-zN6hl49pdN-M3iQ7ttG01KXLA1AEKj9w"
                #handler = ttn.HandlerClient(app_id, access_key)
                #applicationClient = handler.application()
                #applicationClient.register_device(tracker.device_eui, tracker.device_name)
                tracker.user = request.user
                tracker.status = "Ab"
                tracker.save()
                return HttpResponseRedirect('/main/position')
            else:
                return render(request, 'Add.html', {'form': form})
        else:
            form = AddForm()
            return render(request, 'Add.html', {'form': form})
    else:
        return render(request, 'Add.html', {'form': None})

#show a tracker
def showOrEditTracker(request, deviceId):
    if (request.user.is_authenticated):
        tracker = Tracker.objects.get(device_eui = str(deviceId))
        if request.method == 'POST':
            form = AddForm(request.POST, instance=tracker)
            schonVorhanden=False
            if form.is_valid():
                tracker = form.save(commit=False)
                serial_number = form.cleaned_data['device_eui']
                if len(Tracker.objects.filter(device_eui = serial_number)) > 0 and serial_number != str(deviceId):
                    schonVorhanden=True
                if schonVorhanden == True:
                    form.add_error('device_eui',"ID bereits vergeben")
                    return render(request, 'showOrEdit.html', {'form': form})
                else:
                    tracker.user = request.user
                    tracker.save()
                    return HttpResponseRedirect('/main/position')
        else:
            form = AddForm(instance=tracker)
            return render(request, 'showOrEdit.html', {'form': form, 'device_eui': deviceId})
    else:
        return render(request, 'showOrEdit.html', {'form': None})

#remove tracker
def  removeTracker(request, deviceId):
    if (request.user.is_authenticated):
        tracker = Tracker.objects.get(device_eui = str(deviceId))
        tracker.delete()

    return HttpResponseRedirect('/main/position')

def usr(request, template_name="registration/user.html"):
    if (request.user.is_authenticated):
        if request.method == "POST":
            form = UserForm(data=request.POST)
            if form.is_valid():
                if request.user.is_authenticated:
                    user = request.user
                    alleNutzer = User.objects.all()
                    schonVorhanden = False
                    for a in alleNutzer:
                        if a.email == form.cleaned_data['email']:
                            schonVorhanden = True
                    if schonVorhanden == True:
                        form.add_error('email',"Email bereits vergeben")
                        return render(request, 'registration/user.html', {'form': form})
                    else:
                        user.email = form.cleaned_data['email']
                        user.save()
                        return HttpResponseRedirect("/main/position")
        else:
            form = UserForm(instance=request.user)
        return  render(request, 'registration/user.html', {'form': form})
    else:
        return render(request, 'registration/user.html', {'form': None})

def open(request, deviceid):

    GPSTracker = Tracker.objects.get(device_eui=deviceid)
    if GPSTracker.status == "Ra":
        Routen = Route.objects.filter(tracker = GPSTracker, end = None)
        for r in Routen:
            r.end = datetime.now()
            r.save()
        #Leere Routen entfernen
        AlleRouten = Route.objects.filter(tracker=GPSTracker)
        for ar in AlleRouten:
            TrackerPunkte = GPSPoint.objects.filter(tracker = GPSTracker)
            Leer = True
            for tp in TrackerPunkte:
                if (tp.record_date > ar.start and tp.record_date < ar.end):
                    Leer = False
                    break
            if(Leer):
                ar.delete()

    GPSTracker.status='Ge'
    GPSTracker.save()

    return redirect('/main/position')

def close(request, deviceid):
    GPSTracker = Tracker.objects.get(device_eui=deviceid)
    if GPSTracker.status == "Ra":
        Routen = Route.objects.filter(tracker = GPSTracker, end = None)
        for r in Routen:
            r.end = datetime.now()
            r.save()
        # Leere Routen entfernen
        AlleRouten = Route.objects.filter(tracker=GPSTracker)
        for ar in AlleRouten:
            TrackerPunkte = GPSPoint.objects.filter(tracker=GPSTracker)
            Leer = True
            for tp in TrackerPunkte:
                if (tp.record_date > ar.start and tp.record_date < ar.end):
                    Leer = False
                    break
            if (Leer):
                ar.delete()

    GPSTracker.status='Ab'
    GPSTracker.save()
    return redirect('/main/position')

def deleteRoute(request, routeid):
    if (request.user.is_authenticated):
        route = Route.objects.get(id = routeid)
        if (route != None):
            route.delete()

    return redirect('/main/route')


def record(request, deviceid):
    GPSTracker = Tracker.objects.get(device_eui=deviceid)
    GPSTracker.status='Ra'
    GPSTracker.save()
    newroute = Route.objects.create()
    newroute.tracker = GPSTracker
    newroute.start = datetime.now()
    newroute.end = None
    newroute.save()

    return redirect('/main/position')

def position(request):
    if (request.user.is_authenticated):
        GPSTracker = Tracker.objects.filter(user=request.user)
        Punkte = GPSPoint.objects.order_by('record_date')
        Unbestimmte = []
        Bestimmte = []
        for t in GPSTracker:
            if(len(Punkte.filter(tracker = t))<=0):
                Zeile = []
                Zeile.append(t.device_name)
                Zeile.append(t.device_eui)
                Zeile.append(t.get_status_display)
                Zeile.append('None, None')
                Zeile.append('None')
                Zeile.append('Keine Daten')
                if (t.connect_status != 'Off'):
                    t.connect_status='Off'
                    t.save()
                Zeile.append(t.get_connect_status_display)
                Unbestimmte.append(Zeile)
            else:
                Punkt=Punkte.filter(tracker=t).order_by('-record_date')[0]
                Zeile = []
                Zeile.append(t.device_name)
                Zeile.append(t.device_eui)

                Zeile.append(t.get_status_display)
                Zeile.append(str(Punkt.device_lat) + ', ' + str(Punkt.device_long))
                Zeile.append(str(Punkt.device_alt)+' m')
                if (Punkt.record_date != None):
                    zeit = Punkt.record_date
                    Zeile.append(zeit)
                    #weitere Zeile zum sortieren
                    if (datetime.now() - zeit.replace(tzinfo=None) > timedelta(hours=2, minutes=5) and t.connect_status != 'Off'):
                        t.connect_status = 'Off'
                        t.save()
                    Zeile.append(t.get_connect_status_display)
                    Bestimmte.append(Zeile)
                else:
                    Zeile.append("Daten ohne Zeit")
                    if (t.connect_status != 'Off'):
                        t.connect_status = 'Off'
                        t.save()
                    Zeile.append(t.get_connect_status_display)
                    Unbestimmte.append(Zeile)

        for x in Unbestimmte:
            Bestimmte.append(x)

        return render(request,'Standort.html',{'tracker': Bestimmte},{'Kord' : " "})
    else:
        return render(request, 'Standort.html', {'tracker': None}, {'Kord': " "})

def route(request):
    if (request.user.is_authenticated):
        GPSTracker = Tracker.objects.filter(user=request.user).order_by('device_name')
        TrackerRoutenPunkte = []

        for t in GPSTracker:
            #Alle Routen eines Trackers
            Routen = Route.objects.filter(tracker=t).order_by('start')

            #Alle Routen eines Trackers inklusive derer Punkte
            TrackerRouten = []

            for r in Routen:
                RoutenPunkte = []
                if r.end != None:
                    RoutenPunkte = GPSPoint.objects.filter(tracker=t, record_date__range=[r.start, r.end]).order_by('record_date')
                else:
                    RoutenPunkte = GPSPoint.objects.filter(tracker=t, record_date__gte = r.start ).order_by(
                        'record_date')

                #Übergabe der Routen und dessen Punkte in TrackerRouten
                TrackerRouten.append([r.start, r.end, RoutenPunkte, r.id])

            #Übergabe der Tracker Routen in die Auflistung der Tracker
            #Zugriff auf ersten Punkt der ersten Route des Trackers
            #TrackerRoutenPunkte[0][1][2][0]
            if(len(TrackerRouten) > 0):
                TrackerRoutenPunkte.append([t.device_name,TrackerRouten])

        return render(request, 'Route.html',{'tracker':TrackerRoutenPunkte })
    else:
        return render(request, 'Route.html', {'tracker': None})
def statistic(request):
        Punkte = GPSPoint.objects.exclude(device_long=None,device_lat=None)
        PunkteGefiltert = []
        Abstand = 0.0001
        for p in Punkte:
            Doppelt=False
            for pg in PunkteGefiltert:
                if ((float(p.device_long) < float(pg.device_long)+Abstand and float(p.device_long) > float(pg.device_long)-Abstand) and (float(p.device_lat) < float(pg.device_lat)+Abstand and float(p.device_lat) > float(pg.device_lat)-Abstand)):
                    Doppelt = True

            if(Doppelt==False):
                PunkteGefiltert.append(p)

        return render(request, 'Statistic.html', {'punkte': PunkteGefiltert})



