#!/usr/bin/python3
import pymysql
import aprslib
import logging
import argparse
import sys
import threading
import time
import os
import math
import base64
from logging.handlers import TimedRotatingFileHandler

# Command line input
parser = argparse.ArgumentParser(description='Connects to APRS-IS and saves stream to local DB')
parser.add_argument('--callsign', help='Set APRS-IS login callsign', default="nocall")
parser.add_argument('--dbhost', help='Set MySQL host', default="localhost")
parser.add_argument('--dbuser', help='Set MySQL user', default="root")
parser.add_argument('--dbpass', help='Set MySQL password', default="")
parser.add_argument('--db', help='Set MySQL database', default="aprs")
parser.add_argument('--host', help='Set APRS-IS host', default="rotate.aprs.net")
parser.add_argument('--port', help='Set APRS-IS port', default="10152")
parser.add_argument('--filter', help='Set APRS-IS filter', default="")
parser.add_argument('--interval', help='Set APRS-IS heartbeat interval in minutes', default="15")
parser.add_argument('--logfile', help='Set Logfile', default="/var/log/aprs2db.log")
parser.add_argument('--debug', help='Set logging level to DEBUG', action="store_true")

# Parse the arguments
args = parser.parse_args()

def createLog(path, debug=False):
	"""Create a rotating log at the specified path and return logger

	keyword arguments:
	path -- path to log file
	debug -- Boolean to set DEBUG log level,
	"""
	tempLogger = logging.getLogger(__name__)

	# Add handler for rotating file
	handler = TimedRotatingFileHandler(path,
		when="h",
		interval=1,
		backupCount=5)
	tempLogger.addHandler(handler)

	# Add handler for stdout printing
	screenHandler = logging.StreamHandler(sys.stdout)
	tempLogger.addHandler(screenHandler)

	# Set logging level
	if debug:
		tempLogger.setLevel(logging.DEBUG)
	else:
		tempLogger.setLevel(logging.WARNING)

	return tempLogger


def strclean(string):
	"""Escape Special Chars
	
	keyword arguments:
	string -- String Value to Clean
	"""
	#string = string.encode('utf-8')
	string = string.replace("\\", "\\\\")
	string = string.replace("\'", "\\\'")
	string = string.replace("\"", "\\\"")
	return string


def insert2db(packet):
	"""write aprslib packet data to Database (MySQL / MariDB)

	keyword arguments:
	packet -- APRS-IS packet from aprslib connection
	"""
	
	# Define Variables for error prevention
	m_from = m_to = m_symbol = m_symbol_table = m_format = m_via = m_messagecapable = m_latitude = m_longitude = m_gpsfixstatus = m_posAmbiguity = m_altitude = m_speed = m_course = m_comment = m_text = m_path = m_phg = m_rng = m_humidity = m_pressure = m_rain_1h = m_rain_24h = m_rain_since_midnight = m_temperature = m_wind_direction = m_wind_gust = m_wind_speed = m_addresse = m_message_text = m_msgNo = m_response = m_bid = m_identifier = m_timestamp = m_raw_timestamp = m_seq = m_bits = m_analog1 = m_analog2 = m_analog3 = m_analog4 = m_analog5 = m_mbits = m_mtype = m_daodatumbyte = m_alive = m_raw = m_rawb64 = ""
	
	# Extract from
	if "from" in packet:
		m_from = strclean(packet.get("from"))
	
	# Extract to
	if "to" in packet:
		m_to = strclean(packet.get("to"))
		
	# Extract symbol
	if "symbol" in packet:
		m_symbol = strclean(packet.get("symbol"))
		
	# Extract symbol_table
	if "symbol_table" in packet:
		m_symbol_table = strclean(packet.get("symbol_table"))
	
	# Extract format
	if "format" in packet:
		m_format = strclean(packet.get("format"))
		
	# Extract via
	if "via" in packet:
		m_via = strclean(packet.get("via"))
		
	# Extract messagecapable
	if "messagecapable" in packet:
		if packet.get("messagecapable") == True:
			m_messagecapable = "true"
		else:
			m_messagecapable = "false"
	
	# Extract latitude
	if "latitude" in packet:
		m_latitude = packet.get("latitude")
		
	# Extract longitude
	if "longitude" in packet:
		m_longitude = packet.get("longitude")
	
	# Extract gpsfixstatus
	if "gpsfixstatus" in packet:
		m_gpsfixstatus = packet.get("gpsfixstatus")
		
	# Extract posAmbiguity
	if "posAmbiguity" in packet:
		m_posAmbiguity = packet.get("posAmbiguity")
		
	# Extract altitude
	if "altitude" in packet:
		m_altitude = packet.get("altitude")
	
	# Extract speed
	if "speed" in packet:
		m_speed = packet.get("speed")
		
	# Extract course
	if "course" in packet:
		m_course = packet.get("course")
	
	# Extract comment
	if "comment" in packet:
		m_comment = packet.get("comment").encode('unicode-escape').decode('utf-8')
		m_commentb64 = str(base64.b64encode(packet.get("comment").encode("utf-8")), "utf-8")
		
	# Extract text
	if "text" in packet:
		m_text = packet.get("text").encode('unicode-escape').decode('utf-8')
		m_textb64 = str(base64.b64encode(packet.get("text").encode("utf-8")), "utf-8")
	
	# Extract path
	if "path" in packet:
		m_path = strclean(parsePath(packet.get("path")))
		
	# Extract phg
	if "phg" in packet:
		m_phg = packet.get("phg")
		
	# Extract rng
	if "rng" in packet:
		m_rng = packet.get("rng")
	
	# Extract raw packet
	if "raw" in packet:
		m_raw = packet.get("raw").encode('unicode-escape').decode('utf-8')
		encodedBytes = base64.b64encode(packet.get("raw").encode("utf-8"))
		encodedStr = str(encodedBytes, "utf-8")
		m_rawb64 = encodedStr
		
	# Extract weather data
	if "weather" in packet:
		wdata = packet.get("weather")
		#Extract humidity
		if "humidity" in wdata:
			m_humidity = wdata.get("humidity")
		#Extract pressure
		if "pressure" in wdata:
			m_pressure = wdata.get("pressure")
		#Extract rain_1h
		if "rain_1h" in wdata:
			m_rain_1h = wdata.get("rain_1h")
		#Extract rain_24h
		if "rain_24h" in wdata:
			m_rain_24h = wdata.get("rain_24h")
		#Extract rain_since_midnight
		if "rain_since_midnight" in wdata:
			m_rain_since_midnight = wdata.get("rain_since_midnight")
		#Extract temperature
		if "temperature" in wdata:
			m_temperature = wdata.get("temperature")
		#Extract wind_direction
		if "wind_direction" in wdata:
			m_wind_direction = wdata.get("wind_direction")
		#Extract wind_gust
		if "wind_gust" in wdata:
			m_wind_gust = wdata.get("wind_gust")
		#Extract wind_speed
		if "wind_speed" in wdata:
			m_wind_speed = wdata.get("wind_speed")
			
	# Extract message data
	# Extract addresse
	if "addresse" in packet:
		m_addresse = strclean(packet.get("addresse"))
	# Extract message_text
	if "message_text" in packet:
		m_message_text = packet.get("message_text").encode('unicode-escape').decode('utf-8')
		m_message_textb64 = str(base64.b64encode(packet.get("message_text").encode("utf-8")), "utf-8")
	# Extract msgNo
	if "msgNo" in packet:
		m_msgNo = packet.get("msgNo")
	# Extract response
	if "response" in packet:
		m_response = strclean(packet.get("response"))
	
	# Extract bulletin data
	# Extract bid
	if "bid" in packet:
		m_bid = packet.get("bid")
	# Extract identifier
	if "identifier" in packet:
		m_identifier = strclean(packet.get("identifier"))
		
	# Extract status data
	# Extract raw_timestamp
	if "raw_timestamp" in packet:
		m_raw_timestamp = strclean(packet.get("raw_timestamp"))
	# Extract timestamp
	if "timestamp" in packet:
		m_timestamp = packet.get("timestamp")
	
	# Check for tEQNS dictionary
	if "tEQNS" in packet:
		# Exists, initialize channels list and extract equations list
		channels = []
		ddata = packet.get("tEQNS")
		for eqn in ddata:
			# Iterate through each measurement coefficient list, assign to dictionary
			equations = {"a": 0, "b": 0, "c": 0, }
			equations["a"] = eqn[0]
			equations["b"] = eqn[1]
			equations["c"] = eqn[2]
			channels.append(equations)
		if channels:
			telemetryDictionary[m_from] = channels
	
	# Extract telemetry data
	if "telemetry" in packet:
		tdata = packet.get("telemetry")
		#Extract seq
		if "seq" in tdata:
			m_seq = tdata.get("seq")
		#Extract bits
		if "bits" in tdata:
			m_bits = tdata.get("bits")
		
		# Attempt to retrieve scaling values from telemetryDictionary
		try:
			channels = telemetryDictionary[m_from]
		except KeyError:
			# No scaling values found, assign generic scaling to channels
			channels = []
			for eqn in range(5):
				# Create a scaling dictionary for all five measurements
				equations = {"a": 0, "b": 0, "c": 0, }
				equations["a"] = 0
				equations["b"] = 1
				equations["c"] = 0
				channels.append(equations)
		
		# Extract analog values from telemtry packet
		if "vals" in tdata:
			vdata = tdata.get("vals")
			# Apply scaling equation A*V**2 + B*V + C
			# Analog1
			m_analog1 = channels[0]["a"] * math.pow(vdata[0], 2) + channels[0]["b"] * vdata[0] + channels[0]["c"]
			# Analog2
			m_analog2 = channels[1]["a"] * math.pow(vdata[1], 2) + channels[1]["b"] * vdata[1] + channels[1]["c"]
			# Analog3
			m_analog3 = channels[2]["a"] * math.pow(vdata[2], 2) + channels[2]["b"] * vdata[2] + channels[2]["c"]
			# Analog4
			m_analog4 = channels[3]["a"] * math.pow(vdata[3], 2) + channels[3]["b"] * vdata[3] + channels[3]["c"]
			# Analog5
			m_analog5 = channels[4]["a"] * math.pow(vdata[4], 2) + channels[4]["b"] * vdata[4] + channels[4]["c"]
		
	# Extract mic-e data
	# Extract mbits
	if "mbits" in packet:
		m_mbits = packet.get("mbits")
	# Extract mtype
	if "mtype" in packet:
		m_mtype = strclean(packet.get("mtype"))
	if "daodatumbyte" in packet:
		m_daodatumbyte = packet.get("daodatumbyte")
		
	if "alive" in packet:
		m_alive = str(packet.get("alive"))
	
	# Prepare SQL query to INSERT a record into the database.
	sql = "INSERT INTO `packets` (`from`, `to`, `symbol_table`, `symbol`, `format`, `via`, `messagecapable`, `latitude`, `longitude`, `gpsfixstatus`, `posAmbiguity`, `altitude`, `speed`, `course`, `comment`, `text`, `path`, `phg`, `rng`, `humidity`, `pressure`, `rain_1h`, `rain_24h`, `rain_since_midnight`, `temperature`, `wind_direction`, `wind_gust`, `wind_speed`, `addresse`, `message_text`, `msgNo`, `response`, `bid`, `identifier`, `raw_timestamp`, `timestamp`, `seq`, `bits`, `analog1`, `analog2`, `analog3`, `analog4`, `analog5`, `mbits`, `mtype`, `daodatumbyte`, `alive`, `raw`, `rawb64`) VALUES \
	('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}', '{10}', '{11}', '{12}', '{13}', '{14}', '{15}', '{16}', '{17}', '{18}', '{19}', '{20}', '{21}', '{22}', '{23}', '{24}', '{25}', '{26}', '{27}', '{28}', '{29}', '{30}', '{31}', '{32}', '{33}', '{34}', '{35}', '{36}', '{37}', '{38}', '{39}', '{40}', '{41}', '{42}', '{43}', '{44}', '{45}', '{46}', '{47}', '{48}') \
	".format(m_from, m_to, m_symbol_table, m_symbol, m_format, m_via, m_messagecapable, m_latitude, m_longitude, m_gpsfixstatus, m_posAmbiguity, m_altitude, m_speed, m_course, pymysql.escape_string(m_comment), pymysql.escape_string(m_text), m_path, m_phg, m_rng, m_humidity, m_pressure, m_rain_1h, m_rain_24h, m_rain_since_midnight, m_temperature, m_wind_direction, m_wind_gust, m_wind_speed, m_addresse, pymysql.escape_string(m_message_text), m_msgNo, m_response, m_bid, m_identifier, m_raw_timestamp, m_timestamp, m_seq, m_bits, m_analog1, m_analog2, m_analog3, m_analog4, m_analog5, m_bits, m_mtype, m_daodatumbyte, m_alive, pymysql.escape_string(m_raw), m_rawb64)
	
	try:
		# Execute the SQL command
		dbc.execute(sql)
		# Commit your changes in the database
		db.commit()
	except:
		# Rollback in case there is any error
		db.rollback()
		logger.error("Error: unable to write Data to Database", exc_info=True)


def parsePath(path):
	"""Take path and turn into a string

	keyword arguments:
	path -- list of paths from aprslib
	"""

	# Join path items into a string separated by commas, valid line protocol
	temp = ",".join(path)
	pathStr = ("{0}".format(temp))

	# Return line protocol string
	return pathStr
	

def callback(packet):
	"""aprslib callback for every packet received from APRS-IS connection

	keyword arguments:
	packet -- APRS-IS packet from aprslib connection
	"""
	#print("{0}".format(packet))
	logger.info(packet["raw"])
	insert2db(packet)


def consumer(conn):
	"""Start consumer function for thread

	keyword arguments:
	conn -- APRS-IS connection from aprslib
	"""

	logger.debug("starting consumer thread")

	# Send Filter command to APRS-IS Server
	conn.sendall('#filter ' + args.filter + '\r\n')
	
	# Obtain raw APRS-IS packets and sent to callback when received
	conn.consumer(callback, immortal=True, raw=False)


def heartbeat(conn, callsign, interval):
	"""Send out an APRS status message to keep connection alive

	keyword arguments:
	conn -- APRS-IS connction from aprslib
	callsign -- Callsign of status message
	interval -- Minutes between status messages
	"""

	logger.debug("Starting heartbeat thread")
	while True:
		# Create timestamp
		timestamp = int(time.time())

		# Create APRS status message
		status = "{0}>APRS,TCPIP*:>aprs2influxdb heartbeat {1}"
		conn.sendall(status.format(callsign, timestamp))
		logger.debug("Sent heartbeat")

		# Sleep for specified time
		time.sleep(float(interval) * 60) # Sent every interval minutes


def main():
	# Create logger, must be global for functions and threads
	global logger
	
	# Create telemetry dictionary
	global telemetryDictionary
	telemetryDictionary = {}
	
	# Connect to Database
	global dbc
	global db
	# Open database connection
	db = pymysql.connect(args.dbhost,args.dbuser,args.dbpass,args.db)
	# prepare a cursor object using cursor() method
	dbc = db.cursor()
	sql = "SHOW TABLES"
	try:
		# Execute the SQL command
		dbc.execute(sql)
	except:
		logger.error("Error: unable to fetch data", exc_info=True)


	# Log to sys.prefix + aprs2influxdb.log
	if args.logfile != "":
		log = args.logfile
	else:
		log = os.path.join(sys.prefix, "aprs2db.log")
	logger = createLog(log, args.debug)

	# Start login for APRS-IS
	logger.info("Logging into APRS-IS as {0} on port {1}".format(args.callsign, args.port))
	if args.callsign == "nocall":
		logger.warning("APRS-IS ignores the callsign \"nocall\"!")

	# Open APRS-IS connection
	passcode = aprslib.passcode(args.callsign)
	AIS = aprslib.IS(args.callsign,
		passwd=passcode,
		host=args.host,
		port=args.port)

	# Set aprslib logger equal to aprs2influxdb logger
	AIS.logger = logger

	# Connect to APRS-IS servers
	try:
		AIS.connect()

	except aprslib.exceptions.LoginError:
		# An error occured
		logger.error('An aprslib LoginError occured', exc_info=True)

	except aprslib.exceptions.ConnectionError:
		# An error occured
		logger.error('An aprslib ConnectionError occured', exc_info=True)

	# Create heartbeat
	t1 = threading.Thread(target=heartbeat, args=(AIS, args.callsign, args.interval))

	# Create consumer
	t2 = threading.Thread(target=consumer, args=(AIS,))

	# Start threads
	t1.start()
	t2.start()
	

if __name__ == "__main__":
	main()


#db.close()
