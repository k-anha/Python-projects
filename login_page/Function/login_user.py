from data.Queries import *
from data.data_types import *
from sqlite3 import Cursor


# Function to login user
def login_user(
    user_email: Username, user_password: Password, cur: Cursor
) -> tuple[str, str]:
    EMAIL = user_email
    PASSWORD = user_password

    cur.execute(QUERY_TO_LOGIN_USER, (EMAIL, PASSWORD))
    RESULT = cur.fetchone()
    if RESULT:
        return ("Login Successfully", GREEN)
    else:
        return ("Invalid Username or Password\n", RED)
