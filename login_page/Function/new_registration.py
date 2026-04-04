from data.data_types import *
from data.Queries import *

from sqlite3 import IntegrityError, Connection, Cursor


# Function to register new user
def new_registration(
    user_name: Username,
    user_email: EmailID,
    user_password: Password,
    cur: Cursor,
    conn: Connection,
) -> tuple[str, str]:
    NAME = user_name
    EMAIL = user_email
    PASSWORD = user_password

    try:
        cur.execute(QUERY_TO_INSERT_VALUES, (NAME, PASSWORD, EMAIL))
        conn.commit()
        return ("New user registration successfull", GREEN)
    except IntegrityError:
        return ("WARNING Email ID already exists.", YELLOW)
