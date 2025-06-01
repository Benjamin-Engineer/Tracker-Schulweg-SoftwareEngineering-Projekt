import serial
import pynmea2
from dateifunktionen import gps_json_write
from datetime import datetime

starttime = str(datetime.now()) # Startzeit des Programmes

gps = serial.Serial('/dev/ttyAMA0', baudrate=9600, timeout=1)

while True:
    systime = str(datetime.now())
    
    received_data = gps.readline().decode('ascii', errors="replace")
    GPGGA_DATA = received_data.find('$GPGGA,')
    GPRMC_DATA = received_data.find('$GPRMC,')

    if GPGGA_DATA == 0:
        
        msg_local = pynmea2.parse(received_data)
        
        lat = str(msg_local.latitude)
        lon = str(msg_local.longitude)
        
        #print(lat, lon)


    elif GPRMC_DATA == 0:
        
        msg_chrono = pynmea2.parse(received_data)
        
        date = str(msg_chrono.datestamp)
        time = str(msg_chrono.timestamp)
        
        #print(date, time)


    try:
        coord = lat + " " + lon
        gps_json_write(coord, systime, date, starttime) # Koordinaten, Zeit, Ordner, Dateiname
    except:
        gps_json_write("NO SIGNAL", systime, "Error Log", starttime) # Meldung, Zeit, Ordner, Dateiname


