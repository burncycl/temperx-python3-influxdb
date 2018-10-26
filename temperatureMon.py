#!/usr/bin/env python3

# 2018/10 BuRnCycL
# Wrapper for hid-query to write and read raw bytes from /dev/hidrawX TEMPerX device (413d:2107). 
# Converts hex output to binary, and performs calculations to obtain temperature in Celsius and Fahrenheit.   
# Reference: https://github.com/edorfaus/TEMPered/issues/51
# Reference: https://github.com/edorfaus/TEMPered.git # Repo where I grabbed hid-query.
# Built on Raspbery Pi 3 running Raspian Stretch.
# External dependency on hid-query compiled with cmake 
# apt install -y python3 make cmake libhidapi-libusb0 libhidapi-dev libhidapi-hidraw0 libusb-dev libusb-1.0-0
# Note: If you have trouble have trouble with InfluxDB working with the Python library. Use python requests post method.  
# Be sure to update Hard-coded InfluxDBClient variables.


from time import sleep
from influxdb import InfluxDBClient
import datetime, os
from subprocess import Popen, PIPE, STDOUT
#import requests 
# Supress insecure ssl warnings. Because we're using InfluxDB with self-signed certificates.
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class TemperatureMonitor:
    def __init__(self):
        # Declare variables, not war.
        self.client = InfluxDBClient(host='10.1.1.15', port=8086, username='influx', password='S0m3P4ssw0rd', ssl=True, verify_ssl=False, database='statsmon') # Hard-coded InfluxDB details. 

        # Function calls
        self.main()


    def dateTime(self):
        return(datetime.datetime.now()).isoformat()


    def get_temperature(self):
        hidquery_filepath = '{}/TEMPered/utils/hid-query'.format(os.path.dirname(os.path.abspath(__file__))) # Grabs the absolute path of the script directory.
        hidraw_device = '/dev/hidraw1'
        
        cmd = '{} {} 0x01 0x80 0x33 0x01 0x00 0x00 0x00 0x00'.format(hidquery_filepath, hidraw_device)
        p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
        output = p.stdout.readlines() # Read command output.
        output = output[-1].decode('utf-8') # Grab last line in the output, and bytes decode.
        #print(output) # Debugging
        output = output.strip('\n').strip('\t').split(' ') # Strip tab & newline from output.
        output = list(filter(None, output)) # Filter empty list entry.
        #print('{} {} '.format(output[2], output[3])) # Debugging
        
        high_byte = ((int(output[2], 16) << 8)) # Convert high_byte hex to binary and perform bit shift operation.
        low_byte = int(output[3], 16) # Convert low_byte hex to binary.
        #print('{} {} '.format(high_byte, low_byte)) # Debugging
        
        # Calculate temperature.
        celsius_temp = float(int(high_byte + low_byte) / 100) # Add bytes and divide by 100.
        fahrenheit_temp = (float(celsius_temp) * 1.8 + 32)
        
        # Debugging
        #print('{:.2f}C'.format(celsius_temp))
        print('{:.2f}F'.format(fahrenheit_temp))
        return(fahrenheit_temp)


#     def influxdb_requests(self):
#         
#         temperature= int(self.get_temperature())
#         url_string = 'http://localhost:8086/write?db=statsmon' # URL of InfluxDB
#         data_string = 'temperature,device=usb1,location=outside value={}'.format(temperature)
#         
#         r = requests.post(url_string, data=data_string)
   

    def influxdb(self):

        temperature = int(self.get_temperature())
        json_body = [
        {
        "measurement": "temperature",
        "tags": {
            "device": "usb1",
            "location": "outside"
        },
        "time": self.dateTime(),
        "fields": {
            "value": temperature
            }
        }
        ]
        #print(json_body) # Debugging
        self.client.write_points(json_body)


    def main(self):
        while True:
            self.influxdb()
            sleep(30)


TemperatureMonitor()

