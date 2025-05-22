import serial
import pynmea2

gps = serial.Serial('/dev/ttyAMA0', baudrate=9600, timeout=1)
GPPGA_buffer = 0
NMEA_buffer = 0


while True:
             
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