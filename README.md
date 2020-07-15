# aprs2mysql
APRS-IS to MySQL Script inspired by [FaradayRF/aprs2influxdb](https://github.com/FaradayRF/aprs2influxdb)

Supported APRS Packet Formats:
* uncompressed
* mic-e
* object
* compressed
* status
* wx
* beacon
* bulletin
* message

## Getting started
For Using the the tool and connection to the APRS-IS service you need a valid amateur radio license for login you need your callsign.

### Prerequisites
You have to install and configure an [MySQL](https://www.mysql.com/) or [MariDB](https://mariadb.org/) database.

### Installing
Navigate to the source directory and run:

`pip install .`

You also have to copy the [DB schema](https://github.com/japalie/aprs2mysql/blob/master/schema.sql) into the Database.

### Running aprs2mysql
The program uses the default APRS-IS servers (rotate.aprs.net) on the default Port (10152).

#### Command Line Options
`--callsign` Set APRS-IS login callsign ((efault = nocall)
`--dbhost` Set MySQL host (default = localhost)
`--dbuser` Set MySQL user (default = root)
`--dbpass` Set MySQL password (default = )
`--db` Set MySQL database (default = aprs)
`--host` Set APRS-IS host (default = rotate.aprs.net)
`--port` Set APRS-IS port (default = 10152)
`--filter` Set APRS-IS filter (default = "")
`--interval` Set APRS-IS heartbeat interval in minutes (default = 15)
`--logfile` set Logfile (default = /var/log/aprs2db.log)
`--debug` Set logging level to DEBUG (default = False)

#### Example

`aprs2mysql --callsign nocall --dbhost 127.0.0.1 --dbuser root --dbpass '********' --db aprs --host 127.0.0.1 --port 14580 --filter 'p/DL' > /dev/null 2>1 &`

## Deployment
This have been tested on a CentOS/RHEL7 environment.

## Thanks to
* **Bryce Salmi** - *Initial work on aprs2influxdb* - [KB1LQC](https://github.com/kb1lqc)

## Ressources
* [aprs.fi](https://aprs.fi)
* [aprsc](https://github.com/hessu/aprsc)
