Home-Automation
==================

### Christmas Break project:
Design a system to monitor and control the heating system in my home.

### Hardware
The system uses a Raspberry Pi running Raspbian Linux to host the web interface and communicates with an Arduino Mega 2560 and temperature sensors via I2C. 

### Web Interface

#### User Experience

The frontend of the webpage is a set of Radio buttons corresponding to each heating zone in my house. The On and Off settings are applied for one hour from the time they are set. The setting active until column tells when the On/Off setting will expire and revert to the thermostat.
Also an SVG gauge from the google charts API and an SVG tank with the temperatures at three places on the tank.  I'm hoping to add more gauges as I get more temperature sensors installed.

We've got the LG Smart TV setup so with only a couple of clicks the status page can be displayed.

#### Backend Design

The backend is a page that generates the zones & radio buttons using the twig templating engine. The real-time "ness" of the interface is provided using ajax http requests to a cgi python application which acts as an API endpoint, allowing for the setting On/Off each zone and reading each zone. The python api manages the sqlite3 file datastore as well as talking to the arduino and temperature sensors via I2C.

I'm using the arduino as an I2C bridge since the Pi doesn't have the necessary GPIO, which is 2 outputs and 1 input for each zone. We've got 6 zone for a total of 18 GPIO's needed.


### The 1's and 0's
The Pi periodically reads one byte from the Arduino (over I2C) to acquire the status of each of the heating zones.

Writing one byte to the Arduino causes the status of zones to be toggled. The lower four bits are the zone number and the upper two bits represent the state to transition the zone to. Each zone can be in one of three states forced on, forced off, or delegated to the thermostat.﻿

### Photos
Checkout the photos and origional posts on g+ https://plus.google.com/explore/home-automation

### Todos
[] Add graphs of temperature over time
[] Add graphs of when zones are on over time
[] Add a history feature to display when zones were forced On/Off
