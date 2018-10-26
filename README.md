## 2018/10 BuRnCycL

## Objective

Read Temperature data from TEMPerX USB device (413d:2107) (aka TEMPer V26.1) and write data to InfluxDB. Graph temperature data in Grafana.

![TemperX Device](images/temperx_device.jpg?raw=true "TemperX Device")

## Problem 

Ran into issues getting newer versions of TEMPerX device (413d:2107) to work in Python3 on Raspberry Pi. 

Tried using: 
- PyUSB - Complicated and sometimes worked sometimes didn't.
- Python3-hid - Crappy support on Raspian Stretch.

Probably other attempts not mentioned here. All failed horribly and were huge time vampires.

## Solution

Discovered hid-query C program could do the job with some simple hex binary bit shift calculation. Rather than rewrite entirely in C,
decided to write a hacky wrapper for hid-query in Python3.


## Get me going fast


Install dependencies and Compile hid-queyr C library
```
make
```

Update Hard-coded InfluxDBClient Variables in __init__. I know there's better ways to do this.

Install to /usr/local/sbin (should be in $PATH now).
```
make install
```

```
python3 temperatureMon.py
```

Uninstall
```
make uninstall
```

## Build it myself


### Prerequisites

```
apt install -y python3 git
```

### Compile hid-query

Dependencies (assuming you're building on Raspberry Pi or apt package manager based system).
```
apt install -y make cmake libhidapi-libusb0 libhidapi-dev libhidapi-hidraw0 libusb-dev libusb-1.0-0
```

You can grab the latest (If there is a latest. Last I checked it was 5+ years old). Included is a clone from 2018/10.
```
rm -rf ./TEMPered
git clone https://github.com/edorfaus/TEMPered.git
```

Run cmake and make inside cloned ./TEMPered directory
```
cd ./TEMPered
cmake CMakeLists.txt
make
```
You should now have a compiled version of ./TEMPered/utils/hid-query.


### Run python script

Update Hard-coded InfluxDBClient Variables in __init__. I know there's better ways to do this.

```
python3 temperatureMon.py
```


### Example Crontab for watchdog
```
*/5     * * * * root    tempMonWatchdog.sh &> /dev/null
```

### Grafana Settings
![Grafana Query Settings](images/grafana_settings-query.png?raw=true "Grafana Query Settings")
![Grafana Legend Settings](images/grafana_settings-legend.png?raw=true "Grafana Legend Settings")
![Grafana Display Settings](images/grafana_settings-display.png?raw=true "Grafana Display Settings")

References: 
- https://github.com/edorfaus/TEMPered/issues/51
- https://github.com/edorfaus/TEMPered.git # Repo where I grabbed hid-query.

