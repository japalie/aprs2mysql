#!/bin/bash
/usr/bin/python3 /root/aprs.py --callsign TEST --dbhost 127.0.0.1 --dbuser root --dbpass '********' --db aprs --host 127.0.0.1 --port 14580 --filter 'p/HB/OE' > /dev/null 2>1 &