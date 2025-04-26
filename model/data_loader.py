import sqlite3
import pandas as pd
from model.db import get_connection
from datetime import datetime


# ------------- Get data frames -------------------------------
# Functions to collect pd data_frames to pass to the ui components
def get_usernames():               # Default get users query
	conn = get_connection()
	usernames = pd.read_sql_query('SELECT userID AS UserID, name as Names, phone AS Phone FROM user ORDER BY name ASC', conn)
	conn.close()
	return usernames

def get_usernames_filtered(search_name):      # Get users query when search coundition is applied
    conn = get_connection()
    like_pattern = f"%{search_name}%"
    usernames = pd.read_sql_query("""
                                  SELECT userID AS UserID, name as Names, phone AS Phone
                                  FROM user
                                  WHERE name LIKE ?
                                  ORDER BY name ASC
                                  """, conn, params=(like_pattern,))
    conn.close()
    return usernames


def get_bikes():
    conn = get_connection()
    bikes = pd.read_sql_query('SELECT name as Name, status as Status FROM bike ORDER BY bikeID ASC', conn)
    conn.close()
    return bikes

def get_subscription():
	conn = get_connection()
	subs = pd.read_sql_query('SELECT type as Type, count(*) AS Purchased FROM subscription GROUP BY type', conn)
	conn.close()
	return subs

def get_trips_endstation():
    conn = get_connection()
    trips_endstaiton = pd.read_sql_query("""
                                         SELECT station.stationID AS StationID, station.name AS Name, count(*) AS Number_of_trips 
                                         FROM trip JOIN station 
                                         ON trip.endStationID = station.stationID
                                         GROUP BY station.stationID;
                                         """, conn)
    conn.close()
    return trips_endstaiton

def get_station_bikes(query):
    conn = get_connection()
    like_query = f"%{query}%"
    station_bikes = pd.read_sql_query("""SELECT station.name AS Station, bike.name AS Bike 
                                    	FROM station JOIN bike 
                                    	ON station.stationID = bike.lastStationID 
                                    	WHERE bike.status = 'Parked' AND (station.name LIKE ? OR bike.name LIKE ?) 
                                    	ORDER BY station.stationID;
                                     	""", conn, params= (like_query, like_query))
    conn.close()
    return station_bikes

def get_parking_availability(station):
	conn = get_connection()
	availability = pd.read_sql_query("""SELECT name AS Name, ROUND(((availableP_spots * 1.0) / maxP_spots)*100) AS Availability FROM station 
                             		WHERE name = ?;""", conn, params=(station,))
	conn.close()
	return availability    # ava / max * 100%

def get_bike_availability(station): 
	conn = get_connection()
	availability = pd.read_sql_query("""SELECT name AS Name, ROUND((((maxP_spots - availableP_spots) * 1.0)/ maxP_spots)*100) AS Availability FROM station 
                             		WHERE name = ?;""", conn, params=(station,))
	conn.close()
	return availability   # max - ava / max * 100%

 #  ------------- Get lists --------------------
def get_stations(): 
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM station ORDER BY stationID ASC;")
    stations = cursor.fetchall()
    conn.close()
    return [station[0] for station in stations]

def get_users():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM user ORDER BY name ASC;")
    users = cursor.fetchall()
    conn.close()
    return [user[0] for user in users]

def get_repair_choices():
	conn = get_connection()
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM repaircode;")
	codes = cursor.fetchall()
	conn.close()
	choices = {}
	for row in codes:
		choices.update({row[0]:row[1]})
	return choices

 # ------------------ get one ------------------------------
def find_available_bikeID(stationID):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT bike.bikeID
                   FROM bike JOIN station ON bike.lastStationID = station.stationID 
                   WHERE bike.lastStationID = ? AND bike.status = 'Parked' LIMIT 1;""", (stationID,))
    bike = cursor.fetchone()
    conn.close()
    return bike[0] if bike else None

def find_active_bike(userID):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT bike.bikeID FROM bike JOIN trip ON bike.bikeID = trip.bikeID 
                   WHERE trip.userID = ? AND bike.status = 'Active' AND trip.endStationID IS NULL;
                   """, (userID,))
    bike = cursor.fetchone()
    conn.close()
    return bike[0] if bike else None
    

def get_bike_name(bikeID):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM bike WHERE bikeID = ?;", (bikeID,))
    name = cursor.fetchone()
    conn.close()
    return name[0] if name else None

def get_bikeID(name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT bikeID FROM bike WHERE name = ?;", (name,))
    bikeID = cursor.fetchone()
    conn.close()
    return bikeID[0] if bikeID else None

def get_bike_status(bikeID):
	conn = get_connection()
	cursor = conn.cursor()
	cursor.execute("SELECT status FROM bike WHERE bikeID = ?;", (bikeID,))
	status = cursor.fetchone()
	conn.close()
	return status[0] if status else None

def get_userID(name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT userID FROM user WHERE name = ?;", (name,))
    userID = cursor.fetchone()
    conn.close()
    return userID[0] if userID else None

def get_stationID(name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT stationID FROM station WHERE name = ?;", (name,))
    stationID = cursor.fetchone()
    conn.close()
    return stationID[0] if stationID else None

def get_username(userID):
	conn = get_connection()
	cursor = conn.cursor()
	cursor.execute("SELECT name FROM user WHERE userID  = ?;", (userID,))
	name = cursor.fetchone()
	conn.close()
	return name[0] if name else None

def get_station(stationID):
	conn = get_connection()
	cursor = conn.cursor()
	cursor.execute("SELECT name FROM station WHERE stationID  = ?;", (stationID,))
	name = cursor.fetchone()
	conn.close()
	return name[0] if name else None

def get_availability(stationID):
	conn = get_connection()
	cursor = conn.cursor()
	cursor.execute("SELECT availableP_spots FROM station WHERE stationID = ?;", (stationID,))
	availability = cursor.fetchone()
	conn.close()
	return availability[0]

def get_position(station):
	conn = get_connection()
	cursor = conn.cursor()
	cursor.execute("SELECT positionLat, positionLong FROM station WHERE name = ?;", (station,))
	pos = cursor.fetchone()
	conn.close()
	return pos
    

# -------------- Inserts -------------------------------
# Functions to insert new information into the database
def insert_user(full_name, phone_nr, email):
	conn = get_connection()
	cursor = conn.cursor()
	cursor.execute("INSERT INTO user (name, phone, email) VALUES (?, ?, ?)",
				(full_name, phone_nr, email)
				)
	conn.commit()
	conn.close()

def insert_checkout(userID, stationID, bikeID):
    conn = get_connection()
    current_time = datetime.now()
    current_time = current_time.replace(microsecond=0)
    cursor = conn.cursor()
    cursor.execute("UPDATE bike SET status = 'Active' WHERE bikeID = ?", (bikeID,))
    cursor.execute("""INSERT INTO trip (startTime, startStationID, bikeID, userID) VALUES (?, ?, ?, ?)""",
                   (current_time, stationID, bikeID, userID))
    cursor.execute("UPDATE station SET availableP_spots = availableP_spots + 1;")
    conn.commit()
    conn.close()


def insert_dropoff(userID, stationID, bikeID):
    conn = get_connection()
    current_time = datetime.now()
    current_time = current_time.replace(microsecond=0)
    cursor = conn.cursor()
    
    cursor.execute("UPDATE bike SET status = 'Parked', lastStationID = ? WHERE bikeID = ?;", (stationID, bikeID,))
    cursor.execute("UPDATE trip SET endTime = ?, endStationID = ? WHERE userID = ? AND bikeID = ?;",
                   (current_time, stationID, userID, bikeID,))
    cursor.execute("UPDATE station SET availableP_spots = availableP_spots - 1;")
    print("running")
    conn.commit()
    conn.close()
    
def send_repair_request(item, bikeID):
	conn = get_connection()
	cursor = conn.cursor()
	cursor.execute("""
                INSERT INTO repairRequest (bikeID, repaircodeID) VALUES (?, ?);
                """, (bikeID, item))
	cursor.execute("UPDATE bike SET status = 'Inactive' WHERE bikeID = ?;", (bikeID,)) 
	# I could update station availability here if I could guarantee that the bike was removed for repairs imediately, 
	# but it probably will not be. Even setting the bike to Inactive regardles of what repairRequest is sent, is a bit much perhaps.
	# However, since this solution will not take into account what functions would be available to administrators,
 	# I figured this was the best solution to demonstrate that a bike becomes inactive when it is being repaired. 
	conn.commit()
	conn.close()