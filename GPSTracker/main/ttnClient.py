import ttn


app_id = "lorawanvsschloss_11382"
access_key = "ttn-account-v2.8YZ1L3PZAG-zN6hl49pdN-M3iQ7ttG01KXLA1AEKj9w"

def uplink_callback(msg, client):
    from .models import GPSPoint, Tracker
    import traceback
    print(msg)

    try:
        if(len(GPSPoint.objects.filter(tracker__device_eui = msg.hardware_serial).order_by('record_date')) > 0):
            AktuellerStandort = GPSPoint.objects.filter(tracker__device_eui = msg.hardware_serial).order_by('record_date')[0]
        else:
            AktuellerStandort = None
    except Exception:
      traceback.print_exc()


    print(AktuellerStandort)
    AktuellerStandort = None
    try:
        if (AktuellerStandort == None or str(AktuellerStandort.device_long) != str(msg.payload_fields.longitude) or str(AktuellerStandort.device_lat) != str(msg.payload_fields.latitude)):
            print("Neuer Standort")
            #Fall 1: GPS Empfang, Neue Koordinaten-------------------------------------------------------------------------
            if (msg.payload_fields.longitude != 0 or msg.payload_fields.latitude != 0 ):
                #Neue Koordinaten wurden empfangen
                tracker = Tracker.objects.get(device_eui=msg.hardware_serial)

                NewPoint = GPSPoint.objects.create()
                NewPoint.record_date = msg.metadata.time
                NewPoint.tracker = tracker
                NewPoint.device_long = msg.payload_fields.longitude
                NewPoint.device_lat = msg.payload_fields.latitude
                NewPoint.device_alt = msg.payload_fields.altitude
                print(NewPoint.tracker.device_eui)
                NewPoint.save()
                print("New Point Saved to " + tracker.device_eui)
                print(tracker.status)
                print(tracker.connect_status)
                if (tracker.connect_status != 'On'):
                    tracker.connect_status = 'On'
                    tracker.save()
                # senden einer Email im abgeschlossenen Zustand
                if (tracker.status == "Ab"):
                    from email.mime.multipart import MIMEMultipart
                    from email.mime.text import MIMEText
                    import smtplib
                    # create message object instance
                    msg = MIMEMultipart()

                    message = "Der Tracker " + tracker.device_name + " hat eine Bewegung im Abgeschlossenen Zustand gemeldet. " \
                                                                     "Du kannst den Standort hier einsehen: lora1.f2.htw-berlin.de:8080/main/position"

                    # setup the parameters of the message
                    password = "lora12345678"
                    msg['From'] = "lora1.htw.berlin@gmail.com"
                    msg['To'] = tracker.user.email
                    msg['Subject'] = "Achtung! Der GPS Tracker meldet eine Bewegung"

                    # add in the message body
                    msg.attach(MIMEText(message, 'plain'))

                    # create server
                    server = smtplib.SMTP('smtp.gmail.com: 587')

                    server.starttls()

                    # Login Credentials for sending the mail
                    server.login(msg['From'], password)

                    # send the message via the server.
                    server.sendmail(msg['From'], msg['To'], msg.as_string())

                    server.quit()
                    print("Email versendet an " + msg['To'])

            #Fall 2: Kein GPS Empfang-----------------------------------------------------------------------
            else:
                tracker = Tracker.objects.get(device_eui=msg.hardware_serial)
                tracker.connect_status='GPS'
                tracker.save()
                #Wenn zuvor bereits Standort aufgenommen wurde, dessen Zeit aktualisieren
                if (AktuellerStandort != None):
                    AktuellerStandort.record_date = msg.metadata.time
                    AktuellerStandort.save()
                else:
                    #Ansonsten leeren dummy erzeugen um Offline status zu vermeiden
                    NewPoint = GPSPoint.objects.create()
                    NewPoint.record_date = msg.metadata.time
                    NewPoint.tracker = tracker
                    NewPoint.device_long = None
                    NewPoint.device_lat = None
                    NewPoint.device_alt = None
                    NewPoint.save()
                print("Kein GPS Empfang")


        #Fall 3: Standort hat sich nicht geändert-------------------------------------------------------
        else:
            tracker = Tracker.objects.get(device_eui=msg.hardware_serial)
            AktuellerStandort.record_date = msg.metadata.time
            AktuellerStandort.save()
            if (tracker.connect_status != 'On'):
                tracker.connect_status = 'On'
                tracker.save()
            print("Old Points updated")

    except Exception:
        traceback.print_exc()





 # using mqtt client
handler = ttn.HandlerClient(app_id, access_key)
mqtt_client = handler.data()
mqtt_client.set_uplink_callback(uplink_callback)
mqtt_client.connect()
# mqtt_client.close()

# using application manager client
#app_client =  handler.application()
#my_app = app_client.get()
#print(my_app)
#my_devices = app_client.devices()

#print(my_devices)