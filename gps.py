import serial
import pynmea2

gps = serial.Serial('/dev/ttyAMA0', baudrate=9600, timeout=1)
GPPGA_buffer = 0
NMEA_buffer = 0


while True:
             
    received_data = gps.readline().decode('ascii', errors="replace")
    GPGGA_DATA = received_data.find('$GPGGA,')
    GPRMC_DATA = received_data.find('$GPRMC,')
    #print(GPPGGA_DATA)
    if GPGGA_DATA == 0:
        GPGGA_buffer = received_data.split('$GPGGA,',1)[1]
        NMEA_buffer = GPGGA_buffer.split(',')
        
        #print(NMEA_buffer) 
        
        NMEA_time = 0
        NMEA_lat_raw = 0
        NMEA_lon_raw = 0
        
        NMEA_time = NMEA_buffer[0] #extracts time for NMEA-Data
        
        msg_local = pynmea2.parse(received_data)
        
        lat = msg_local.latitude
        lon = msg_local.longitude
        
        
    elif GPRMC_DATA == 0:
        msg_chrono = pynmea2.parse(received_data)
        
        date = msg_chrono.datestamp
        time = msg_chrono.timestamp