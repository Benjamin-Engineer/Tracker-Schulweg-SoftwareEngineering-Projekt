import serial
import sys

gps = serial.Serial('/dev/ttyAMA0', baudrate=9600, timeout=1)
GPPGA_buffer = 0
NMEA_buffer = 0




while True:
             
    received_data = gps.readline().decode('ascii', errors="replace")
    GPPGGA_DATA = received_data.find('$GPGGA,')
    #print(GPPGGA_DATA)
    if GPPGGA_DATA == 0:
        GPGGA_buffer = received_data.split('$GPGGA,',1)[1]
        NMEA_buffer = GPGGA_buffer.split(',')
        
        #print(NMEA_buffer) 
        
        NMEA_time = 0
        NMEA_lat_raw = 0
        NMEA_lon_raw = 0
        
        NMEA_time = NMEA_buffer[0] #extracts time for NMEA-Data
        print(NMEA_time)
        
        NMEA_lat = NMEA_buffer[1]
        NMEA_lon = NMEA_buffer[3]
        
        print('Latraw: ', NMEA_lat, ' Lonraw: ',NMEA_lon)
        