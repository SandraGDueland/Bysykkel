import sqlite3
from config import DATABASE_PATH

def get_connection():
    return sqlite3.connect(DATABASE_PATH)


# -------------------------------------------------------------------------------------------------------------------------------------
# 1. Creating the DB tables in terminal:
# sqlite3 bysykkel.db
# CREATE TABLE user (userID INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, phone TEXT, positionLat TEXT, positionLong TEXT, email TEXT);
# CREATE TABLE subscription (subscriptionID INTEGER PRIMARY KEY AUTOINCREMENT, type TEXT, startTime DATATIME, userID REFERENCES user (userID));
# CREATE TABLE station (stationID INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, positionLat TEXT, positionLong TEXT, maxP_spots INT, availableP_spots INT);
# CREATE TABLE bike (bikeID INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, status TEXT, lastStationID REFERENCES station (stationID));
# CREATE TABLE trip (tripID INTEGER PRIMARY KEY AUTOINCREMENT, startTime DATETIME, endTime DATETIME, startStationID REFERENCES station (stationID), endStationID REFERENCES station (stationID), bikeID REFERENCES bike (bikeID), userID REFERENCES user (userID));
# CREATE TABLE repaircode (repaircode INT PRIMARY KEY, description TEXT);
# CREATE TABLE repairRequest (repairRequestID INTEGER PRIMARY KEY AUTOINCREMENT, bikeID REFERENCES bike (bikeID), repaircodeID REFERENCES repaircode (repaircodeID));

# -------------------------------------------------------------------------------------------------------------------------------------
# 2. Populating the tables:

# import pandas as pd
# import sqlite3

# csv_file = 'bysykkel.csv'
# df = pd.read_csv(csv_file)

# conn = sqlite3.connect('bysykkel.db')
# cursor = conn.cursor()

# for _, row in df.iterrows():
#     userID = row['user_id']
#     if not (userID > 0):    
#         print('userID NULL: ', userID)
#         continue
#     cursor.execute('''
#     INSERT OR IGNORE INTO user (userID, name, phone) VALUES (?, ?, ?)
#     ''', (userID, row['user_name'], str(int(row['user_phone_number']))))

# for _, row in df.iterrows():
#     subscriptionID = row['subscription_id']
#     if not (subscriptionID > 0):
#         print('subscriptionID NULL: ', subscriptionID)
#         continue
#     cursor.execute(''' 
#     INSERT OR IGNORE INTO subscription (subscriptionID, type, startTime, userID) VALUES (?, ?, ?, ?)
#     ''', (subscriptionID, row['subscription_type'], row['subscription_start_time'], row['user_id']))

# for _, row in df.iterrows():
#     stationID = row['start_station_id']
#     if not (stationID > 0): 
#         print('stationID NULL: ', stationID)
#         continue
#     cursor.execute(''' 
#     INSERT OR IGNORE INTO station (stationID, name, positionLat, positionLong, maxP_spots, availableP_spots) VALUES (?, ?, ?, ?, ?, ?)
#     ''', (stationID, row['start_station_name'], row['start_station_latitude'], row['start_station_longitude'], row['start_station_max_spots'], row['satart_station_available_spots']))
   
# for _, row in df.iterrows():
#     bikeID = row['bike_id']
#     if not(bikeID > 0):
#         print('bikeID NULL', bikeID)
#         continue
#     cursor.execute('''
#     INSERT OR IGNORE INTO bike (bikeID, name, status, lastStationID) VALUES (?, ?, ?, ?)
#     ''', (bikeID, row['bike_name'], row['bike_status'], row['bike_station_id']))

# for _, row in df.iterrows():
#     tripID = row['trip_id']
#     if not(tripID > 0):
#         print('tripID NULL:', tripID)
#         continue
#     cursor.execute('''
#     INSERT OR IGNORE INTO trip (tripID, startTime, endTime, startStationID, endStationID, bikeID, userID) VALUES (?, ?, ?, ?, ?, ?, ?)
#     ''', (tripID, row['trip_start_time'], row['trip_end_time'], row['start_station_id'], row['end_station_id'], row['bike_id'], row['user_id'])) 

# conn.commit()
# conn.close()