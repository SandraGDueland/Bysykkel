import sqlite3
from config import DATABASE_PATH

def get_connection():
    return sqlite3.connect(DATABASE_PATH)


# Exercise 1c)
# user ALTER TABLE directly in terminal to add a column 'email' to user table in the db