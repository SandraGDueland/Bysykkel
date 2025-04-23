import sqlite3
import pandas as pd
from model.db import get_connection


# Functions to collect pd data_frames to pass to the ui components
def get_usernames():
	conn = get_connection()
	usernames = pd.read_sql_query('SELECT userID AS UserID, name as Names, phone AS Phone FROM user ORDER BY name ASC', conn)
	conn.close()
	return usernames

def get_usernames_filtered(search_name):
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


# Functions to insert new information into the database
def insert_user(full_name, phone_nr, email):
	conn = get_connection()
	cursor = conn.cursor()
	cursor.execute("INSERT INTO user (name, phone, email) VALUES (?, ?, ?)",
				(full_name, phone_nr, email)
				)
	conn.commit()
	conn.close()
