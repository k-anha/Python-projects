#sabse pehle to apna database ban lo
from Function.new_registration import *
from Function.color_text import *
from Function.login_user import *

# Importing sqlite library
import sqlite3

# Creating connection and cursor to execute queries
conn = sqlite3.connect("database.db")
cur = conn.cursor()

# Query to create table if exists
# cur.execute("DROP TABLE IF EXISTS CREDENTIALS")
# QUERY_TO_CREATE_TABLE = """ CREATE TABLE CREDENTIALS (
#     ID INTEGER PRIMARY KEY AUTOINCREMENT,
#     USERNAME TEXT NOT NULL,
#     PASSWORD TEXT NOT NULL,
#     EMAIL TEXT UNIQUE NOT NULL
#     ) """
# cur.execute(QUERY_TO_CREATE_TABLE)
# print("Table created successfully")
while True:
    print("1. New User :")
    print("2. Login User :")
    print("3. Exit User :")

    # Getting user input
    user_input = int(input("Enter your choice :"))

    # If user input is 1, then take parameters and make new registration
    if user_input == 1:
        user_name = input("Enter your name :")
        user_email = input("Enter your email :")
        user_password = input("Enter password :")

        response: tuple[str, str] = new_registration(
            user_name, user_email, user_password, cur, conn   
        )

#
        response_message, response_status = response

        color_text(response_message, response_status)

        break

    # If user input is 2 then logging user by taking parameters
    elif user_input == 2:
        user_email = input("Enter your email :")
        user_password = input("Enter password :")

        response: tuple[str, str] = login_user(user_email, user_password, cur)

        response_message, response_status = response

        color_text(response_message, response_status)

        break

    # If user input is 3 then closing connection and database
    elif user_input == 3:
        cur.close()
        conn.close()
        color_text("Exit successfully", GREEN)
        break

    # If any other input then print Invalid Choice
    else:
        color_text("Invalid choice", RED)
